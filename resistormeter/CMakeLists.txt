cmake_minimum_required(VERSION 3.12)

# Pull in SDK (must be before project)
include(pico_sdk_import.cmake)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

set(PICO_EXAMPLES_PATH ${PROJECT_SOURCE_DIR})

# Initialize the SDK
pico_sdk_init()

project(resistormeter)

add_executable(resistormeter resistormeter.c)

# Pull in our pico_stdlib which pulls in commonly used features
target_link_libraries(resistormeter hardware_adc pico_stdlib)

pico_enable_stdio_usb(resistormeter 0)
pico_enable_stdio_uart(resistormeter 1)

# create map/bin/hex file etc.
pico_add_extra_outputs(resistormeter)
