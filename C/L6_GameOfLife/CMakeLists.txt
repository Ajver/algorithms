cmake_minimum_required(VERSION 3.10)
project(GameOfLife C)

set(CMAKE_C_STANDARD 99)

# katalog, w którym będą zapisywane pliki bibliotek statycznych
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# biblioteka statyczna
add_library(game_of_life_library STATIC
    src/game_of_life.c
)

# plik wykonywalny
add_executable(app src/main.c)

# połącz bibliotekę z plikiem wykonywalnym
target_link_libraries(app game_of_life_library)