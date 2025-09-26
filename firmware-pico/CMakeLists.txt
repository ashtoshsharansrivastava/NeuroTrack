cmake_minimum_required(VERSION 3.13)

# Initialize the pico-sdk from the environment variable
include($ENV{PICO_SDK_PATH}/pico_sdk_init.cmake)

project(neurotrack_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the SDK for our project
pico_sdk_init()

# Define our executable and the source file it uses
add_executable(neurotrack_project
  sketch.cpp
)

# Link the standard Pico libraries and the ADC library
target_link_libraries(neurotrack_project pico_stdlib hardware_adc)

# --- CRUCIAL STEP ---
# This line enables the USB serial communication library
pico_enable_stdio_usb(neurotrack_project 1)
pico_enable_stdio_uart(neurotrack_project 0)

# This is required for the Wokwi simulation to generate the final files
pico_add_extra_outputs(neurotrack_project)

