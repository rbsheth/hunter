# Copyright (c) 2016-2019, Ruslan Baratov
# All rights reserved.

cmake_minimum_required(VERSION 3.2)

# Emulate HunterGate:
# * https://github.com/hunter-packages/gate
#include("../common.cmake")
include(HunterGate.cmake)
HunterGate(
    URL "https://github.com/ruslo/hunter/archive/v0.23.151.tar.gz"
    SHA1 "68657b81508c2d3c248731b5a0c2125f19866721"
)

project(download-libzip)

# DOCUMENTATION_START {
hunter_add_package(libzip)
find_package(libzip CONFIG REQUIRED)

add_executable(boo boo.cpp)
target_link_libraries(boo PUBLIC libzip::zip)
# DOCUMENTATION_END }
