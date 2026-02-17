cmake_minimum_required(VERSION 3.15)
project(clox)

# Generate compile_commands.json
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set C standard
set(CMAKE_C_STANDARD 99)

# Set compiler flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -g")

# Force clang as compiler
set(CMAKE_C_COMPILER clang)

# Define source files
set(SOURCES chunk.c debug.c main.c memory.c value.c)

# Define header files (optional for CMake, but good for IDE integration)
set(HEADERS chunk.h common.h debug.h memory.h value.h)

# Add executable
add_executable(clox ${SOURCES} ${HEADERS})

add_executable(chunk_test)

target_sources(chunk_test PRIVATE chunk_test.c chunk.c munit.c memory.c value.c)

# Debug configuration
set_target_properties(clox PROPERTIES DEBUG_POSTFIX "_debug")
