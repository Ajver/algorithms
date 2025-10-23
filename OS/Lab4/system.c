#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    unsigned int pid = getpid();
    
    printf("hello, I'm System program! My PID = %d\n", pid);

    system("gcc another.c -o another.out && ./another.out");

    unsigned int new_pid = getpid();
    printf("Hi again from system program! My current PID = %d\n", new_pid);
    printf("Is PID the same as before? %s\n", pid == new_pid ? "yes" : "no");

    return 0;
}
