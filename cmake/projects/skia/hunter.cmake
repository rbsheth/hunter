# Copyright (c) 2020, Rahul Sheth
# All rights reserved.

# !!! DO NOT PLACE HEADER GUARDS HERE !!!

include(hunter_add_version)
include(hunter_cacheable)
include(hunter_cmake_args)
include(hunter_download)
include(hunter_pick_scheme)

hunter_add_version(
    PACKAGE_NAME
    skia
    VERSION
    75-p0
    URL
    "https://github.com/cpp-pm/skia/archive/v75-p0.tar.gz"
    SHA1
    ae9e1e067af78380eb3f858bbf50cc482ff4aca2
)

hunter_cmake_args(
    skia
    CMAKE_ARGS
         SKIA_BUILD_MODULE_SKSHAPER=ON
         SKIA_ENABLE_ATLAS_TEXT=ON
         SKIA_ENABLE_OPENCL=OFF
         SKIA_ENABLE_VULKAN=OFF
         SKIA_STATIC=ON
         SKIA_SHARED=OFF
)

hunter_pick_scheme(DEFAULT url_sha1_cmake)
hunter_cacheable(skia)
hunter_download(PACKAGE_NAME skia)

