# Copyright (c) 2016-2019, Ruslan Baratov
# All rights reserved.

# !!! DO NOT PLACE HEADER GUARDS HERE !!!

include(hunter_add_version)
include(hunter_cacheable)
include(hunter_download)
include(hunter_pick_scheme)

hunter_add_version(
    PACKAGE_NAME
    zip
    VERSION
    0.1.14-t2
    URL
    "https://github.com/rbsheth/zip/archive/v0.1.14-t2.tar.gz"
    SHA1
    4f031300cbafb7b07f67724f21207d78ff7a8d75
)

hunter_pick_scheme(DEFAULT url_sha1_cmake)
hunter_cacheable(zip)
hunter_download(PACKAGE_NAME zip)
