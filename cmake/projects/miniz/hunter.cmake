# Copyright (c) 2016-2019, Ruslan Baratov
# All rights reserved.

# !!! DO NOT PLACE HEADER GUARDS HERE !!!

include(hunter_add_version)
include(hunter_cacheable)
include(hunter_download)
include(hunter_pick_scheme)
include(hunter_cmake_args)

hunter_add_version(
    PACKAGE_NAME
    miniz
    VERSION
    2.0.8-a426483-t1
    URL
    "https://github.com/rbsheth/miniz/archive/v2.0.8-a426483-t1.tar.gz"
    SHA1
    02f16b66c69fe751de75929a3d64075868d03a2d
)

hunter_cmake_args(miniz
   CMAKE_ARGS
       BUILD_EXAMPLES=OFF
       BUILD_HEADER_ONLY=ON
)

hunter_pick_scheme(DEFAULT url_sha1_cmake)
hunter_cacheable(miniz)
hunter_download(PACKAGE_NAME miniz)
