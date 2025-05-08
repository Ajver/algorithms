cmake_minimum_required(VERSION 3.10)
project(IntegrationDynamic C)

set(CMAKE_C_STANDARD 99)

# biblioteka dynamiczną (shared)
add_library(integration_lib SHARED src/function.c src/integrate.c)

# zmienna dla eksportu na Windows
target_compile_definitions(integration_lib PRIVATE BUILD_INTEGRATION)

# plik wykonywalny
add_executable(app src/main.c)

# linkowana aplikacja z biblioteką dynamiczną
target_link_libraries(app integration_lib)
target_link_libraries(app m)

