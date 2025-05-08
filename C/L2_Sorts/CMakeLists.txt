cmake_minimum_required(VERSION 3.10)
project(SortsLib C)

set(CMAKE_C_STANDARD 99)

# katalog, w którym będą zapisywane pliki bibliotek statycznych
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# biblioteka statyczna
add_library(sort_library STATIC
        src/bubble_sort.c
        src/insertion_sort.c
        src/quick_sort.c
        src/merge_sort.c
)

# plik wykonywalny
add_executable(sorts_app src/main.c)

# połącz bibliotekę z plikiem wykonywalnym
target_link_libraries(sorts_app sort_library)

