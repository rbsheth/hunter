# Copyright (c) 2020, Rahul Sheth
# All rights reserved.

cmake_minimum_required(VERSION 3.2)

set(TESTING_CONFIG_OPT FILEPATH ${CMAKE_CURRENT_LIST_DIR}/config.cmake)

# Emulate HunterGate:
# * https://github.com/hunter-packages/gate
include("../common.cmake")

project(download-skia)

# DOCUMENTATION_START {
hunter_add_package(skia)
find_package(skia CONFIG REQUIRED)

add_executable(boo boo.cpp)
target_link_libraries(boo PUBLIC skia::skia)
# DOCUMENTATION_END }
