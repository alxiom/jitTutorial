cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(custom_ops)

find_package(Torch REQUIRED)

include_directories(/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/include)
include_directories(/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/include/darwin)

add_executable(ModelBin Model.cpp)
add_library(Model SHARED Model.cpp)
target_link_libraries(ModelBin "${TORCH_LIBRARIES}")
target_link_libraries(Model "${TORCH_LIBRARIES}")
set_property(TARGET ModelBin PROPERTY CXX_STANDARD 11)
set_property(TARGET Model PROPERTY CXX_STANDARD 11)