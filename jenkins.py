#!/usr/bin/env python3

# Copyright (c) 2014, Ruslan Baratov
# All rights reserved.

# https://github.com/cpp-pm/polly/wiki/Jenkins

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from enum import Enum

class CI(Enum):
  NONE = 'none'
  TRAVIS = 'travis'
  APPVEYOR = 'appveyor'

class BuildType(Enum):
  PUSH = 'push'
  PR = 'pr'

def clear_except_download(hunter_root):
  base_dir = os.path.join(hunter_root, '_Base')
  if os.path.exists(base_dir):
    print('Clearing directory: {}'.format(base_dir))
    hunter_download_dir = os.path.join(base_dir, 'Download', 'Hunter')
    if os.path.exists(hunter_download_dir):
      shutil.rmtree(hunter_download_dir)
    for filename in os.listdir(base_dir):
      if filename != 'Download':
        to_remove = os.path.join(base_dir, filename)
        if os.name == 'nt':
          # Fix "path too long" error
          subprocess.check_call(['cmd', '/c', 'rmdir', to_remove, '/S', '/Q'])
        else:
          shutil.rmtree(to_remove)

def get_build_type(ci_type):
  if ci_type == CI.TRAVIS:
    return BuildType.PUSH if os.environ.get('TRAVIS_PULL_REQUEST', None) == 'false' else BuildType.PR
  elif ci_type == CI.APPVEYOR:
    return BuildType.PUSH if not os.environ.get('APPVEYOR_PULL_REQUEST_NUMBER', None) else BuildType.PR
  else:
    assert 0, 'Build type only available in CI'

def get_changed_files(ci_type, build_type):
  if build_type == BuildType.PUSH:
    # Push builds are only allowed on master, so this must be a post-merge build.
    # Always assume squash merges only.
    return subprocess.check_output('git diff --name-only HEAD~1..'.split()).decode().splitlines()
  elif build_type == BuildType.PR:
    target_branch = os.environ['TRAVIS_BRANCH'] if ci_type == CI.TRAVIS else os.environ['APPVEYOR_REPO_BRANCH']
    fetch_command = 'git fetch origin {}'.format(target_branch)
    print(fetch_command)

    print("Fetching cpp-pm/master...\n")
    subprocess.check_call(fetch_command.split())
    return subprocess.check_output('git diff --name-only FETCH_HEAD...'.split()).decode().splitlines()
  else:
    assert 0, 'Unknown build type'

def get_project_dirs(current_dir, ci_type):
  project_dir = os.getenv('PROJECT_DIR')
  if not project_dir:
    build_type = get_build_type(ci_type)
    print('Build type: ', build_type)

    changed_files = get_changed_files(ci_type, build_type)
    print('Changed files:\n', changed_files)

    project_dirs = []
    for changed_file in changed_files:
      if changed_file.startswith('examples/'):
        project_dir = changed_file.split('/')[1]
        project_dirs.append(os.path.join('examples', project_dir))
      elif changed_file.startswith('cmake/projects/'):
        project_dir = changed_file.split('/')[2]
        project_dirs.append(os.path.join('examples', project_dir))
  else:
    project_dirs = [project_dir]

  print('Project dirs: \n', project_dirs)

  return [os.path.normpath(os.path.join(current_dir, x)) for x in project_dirs]

def run():
  parser = argparse.ArgumentParser("Testing script")
  parser.add_argument(
      '--nocreate',
      action='store_true',
      help='Do not create Hunter archive (reusing old)'
  )
  parser.add_argument(
      '--all-release',
      action='store_true',
      help='Release build type for all 3rd party packages'
  )
  parser.add_argument(
      '--clear',
      action='store_true',
      help='Remove old testing directories'
  )
  parser.add_argument(
      '--clear-except-download',
      action='store_true',
      help='Remove old testing directories except `Download` directory'
  )
  parser.add_argument(
      '--disable-builds',
      action='store_true',
      help='Disable building of package (useful for checking package can be loaded from cache)'
  )
  parser.add_argument(
      '--upload',
      action='store_true',
      help='Upload cache to server and run checks (clean up will be triggered, same as --clear-except-download)'
  )

  parsed_args = parser.parse_args()

  if parsed_args.upload:
    password = os.getenv('GITHUB_USER_PASSWORD')
    if password is None:
      sys.exit('Expected environment variable GITHUB_USER_PASSWORD on uploading')

  cdir = os.getcwd()
  hunter_root = cdir

  toolchain = os.getenv('TOOLCHAIN')
  if not toolchain:
    sys.exit('Environment variable TOOLCHAIN is empty')

  if os.getenv('TRAVIS'):
    ci_type = CI.TRAVIS
  elif os.getenv('APPVEYOR'):
    ci_type = CI.APPVEYOR
  else:
    ci_type = CI.NONE
  print('CI: ', ci_type)

  if ci_type is not CI.NONE and toolchain == 'dummy':
    print('Skip build: CI dummy (workaround)')
    sys.exit(0)

  project_dirs = get_project_dirs(cdir, ci_type)

  verbose = True
  env_verbose = os.getenv('VERBOSE')
  if env_verbose:
    if env_verbose == '0':
      verbose = False
    elif env_verbose == '1':
      verbose = True
    else:
      sys.exit(
          'Environment variable VERBOSE: expected 0 or 1, got "{}"'.format(
              env_verbose
          )
      )

  testing_dir = os.path.join(os.getcwd(), '_testing')
  if os.path.exists(testing_dir) and parsed_args.clear:
    print('REMOVING: {}'.format(testing_dir))
    shutil.rmtree(testing_dir)
  os.makedirs(testing_dir, exist_ok=True)

  if os.name == 'nt':
    # path too long workaround
    hunter_junctions = os.getenv('HUNTER_JUNCTIONS')
    if hunter_junctions:
      temp_dir = tempfile.mkdtemp(dir=hunter_junctions)
      shutil.rmtree(temp_dir)
      subprocess.check_output(
          "cmd /c mklink /J {} {}".format(temp_dir, testing_dir)
      )
      testing_dir = temp_dir

  hunter_url = os.path.join(testing_dir, 'hunter.tar.gz')

  if parsed_args.nocreate:
    if not os.path.exists(hunter_url):
      sys.exit('Option `--nocreate` but no archive')
  else:
    arch = tarfile.open(hunter_url, 'w:gz')
    arch.add('cmake')
    arch.add('scripts')
    arch.close()

  hunter_sha1 = hashlib.sha1(open(hunter_url, 'rb').read()).hexdigest()

  hunter_root = os.path.join(testing_dir, 'Hunter')

  if parsed_args.clear_except_download:
    clear_except_download(hunter_root)

  if os.name == 'nt':
    which = 'where'
  else:
    which = 'which'

  polly_root = os.getenv('POLLY_ROOT')
  if polly_root:
    polly_root = os.path.abspath(polly_root)
    print('Using POLLY_ROOT: {}'.format(polly_root))
    build_script = os.path.join(polly_root, 'bin', 'build.py')
  else:
    build_script = subprocess.check_output(
        [which, 'build.py'], universal_newlines=True
    ).split('\n')[0]

  if not os.path.exists(build_script):
    sys.exit('Script not found: {}'.format(build_script))

  print('Testing in: {}'.format(testing_dir))
  os.chdir(testing_dir)

  project_dir_index = 8
  args = [
      sys.executable,
      build_script,
      '--clear',
      '--config',
      'Release',
      '--toolchain',
      toolchain,
      '--home',
      'PROJECT_DIR_PLACEHOLDER',
      '--fwd',
      'CMAKE_POLICY_DEFAULT_CMP0069=NEW',
      'HUNTER_SUPPRESS_LIST_OF_FILES=ON',
      'HUNTER_ROOT={}'.format(hunter_root),
      'TESTING_URL={}'.format(hunter_url),
      'TESTING_SHA1={}'.format(hunter_sha1)
  ]

  if not parsed_args.nocreate:
    args += ['HUNTER_RUN_INSTALL=ON']

  if parsed_args.disable_builds:
    args += ['HUNTER_DISABLE_BUILDS=ON']

  if parsed_args.all_release:
    args += ['HUNTER_CONFIGURATION_TYPES=Release']

  if parsed_args.upload:
    passwords = os.path.join(
        cdir, 'maintenance', 'upload-password-template.cmake'
    )
    args += ['HUNTER_RUN_UPLOAD=ON']
    args += ['HUNTER_PASSWORDS_PATH={}'.format(passwords)]

  args += ['--verbose']
  if not verbose:
    args += ['--discard', '10']
    args += ['--tail', '200']

  for project_dir in project_dirs:
    args[project_dir_index] = project_dir

    print('Testing: ', project_dir, '\n\n\n')
    print('Execute command: [')
    for i in args:
      print('  `{}`'.format(i))
    print(']')

    subprocess.check_call(args)

  if parsed_args.upload:
    assert len(project_dirs) == 1, 'Upload can only be used on one package at a time'
    project_dir = project_dirs[0]

    seconds = 60
    print(
        'Wait for GitHub changes became visible ({} seconds)...'.format(seconds)
    )
    time.sleep(seconds)

    print('Run sanity build')

    clear_except_download(hunter_root)

    # Sanity check - run build again with disabled building from sources
    args = [
        sys.executable,
        build_script,
        '--clear',
        '--verbose',
        '--config',
        'Release',
        '--toolchain',
        toolchain,
        '--home',
        project_dir,
        '--fwd',
        'HUNTER_DISABLE_BUILDS=ON',
        'HUNTER_USE_CACHE_SERVERS=ONLY',
        'CMAKE_POLICY_DEFAULT_CMP0069=NEW',
        'HUNTER_SUPPRESS_LIST_OF_FILES=ON',
        'HUNTER_ROOT={}'.format(hunter_root),
        'TESTING_URL={}'.format(hunter_url),
        'TESTING_SHA1={}'.format(hunter_sha1)
    ]
    if not verbose:
      args += ['--discard', '10']
      args += ['--tail', '200']

    print('Execute command: [')
    for i in args:
      print('  `{}`'.format(i))
    print(']')

    subprocess.check_call(args)

if __name__ == "__main__":
  run()
