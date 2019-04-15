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
    libzip
    VERSION
    1.5.2a-e495cd-t3
    URL
    "https://github.com/rbsheth/libzip/archive/v1.5.2a-e495cd-t3.tar.gz"
    SHA1
    a0967b7228c43a43063079596d68a9c8370a3333
)

hunter_cmake_args(
    libzip
    CMAKE_ARGS
        ENABLE_COMMONCRYPTO=OFF
        ENABLE_GNUTLS=OFF
        ENABLE_MBEDTLS=OFF
        ENABLE_WINDOWS_CRYPTO=OFF
        BUILD_TOOLS=OFF
        BUILD_REGRESS=OFF
        BUILD_EXAMPLES=OFF
        BUILD_DOC=OFF
        BUILD_SHARED_LIBS=OFF
)

hunter_pick_scheme(DEFAULT url_sha1_cmake)
hunter_cacheable(libzip)
hunter_download(PACKAGE_NAME libzip)
