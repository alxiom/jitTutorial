cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(custom_ops)

find_package(Torch REQUIRED)

add_executable(modelBin model.cpp)
add_library(Model SHARED model.cpp)
target_link_libraries(modelBin "${TORCH_LIBRARIES}")
target_link_libraries(Model "${TORCH_LIBRARIES}")
set_property(TARGET modelBin PROPERTY CXX_STANDARD 11)
set_property(TARGET Model PROPERTY CXX_STANDARD 11)