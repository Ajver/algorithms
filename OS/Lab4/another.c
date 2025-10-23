#include <stdio.h>
#include <unistd.h>

int main() {
    unsigned int pid = getpid();
    
    printf("hello, I'm another program! My PID = %d\n", pid);

    return 0;
}