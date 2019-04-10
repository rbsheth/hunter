# Copyright (c) 2016-2019, Ruslan Baratov
# All rights reserved.

# !!! DO NOT PLACE HEADER GUARDS HERE !!!

include(hunter_add_version)
include(hunter_cacheable)
include(hunter_download)
include(hunter_pick_scheme)

hunter_add_version(
    PACKAGE_NAME
    miniz
    VERSION
    2.0.8-b493652-t2
    URL
    "https://github.com/rbsheth/miniz/archive/v2.0.8-b493652-t2.tar.gz"
    SHA1
    46582528e1c9ebb0d6fe021a09406473e4d5931e
)

hunter_pick_scheme(DEFAULT url_sha1_cmake)
hunter_cacheable(miniz)
hunter_download(PACKAGE_NAME miniz)
