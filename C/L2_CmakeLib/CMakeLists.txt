cmake_minimum_required(VERSION 3.10)
project(HelloLibrary C)

set(CMAKE_C_STANDARD 99)

# katalog, w którym będą zapisywane pliki bibliotek statycznych
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# dodaj bibliotekę
add_library(hello_library src/hello.c)

# plik wykonywalny
add_executable(hello_app src/main.c)

# połącz bibliotekę z plikiem wykonywalnym
target_link_libraries(hello_app hello_library)
