#ifndef HELLO_H
#define HELLO_H

#ifdef _WIN32
    #ifdef BUILD_HELLO
        #define HELLO_API __declspec(dllexport)
    #else
        #define HELLO_API __declspec(dllimport)
    #endif
#else
    #define HELLO_API
#endif

HELLO_API void hello_world();

#endif
