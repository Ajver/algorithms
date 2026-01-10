// gcc z13_2.c -o z13_2.o -lm && ./z13_2.o

#include <stdio.h>
#include <math.h>

static unsigned long next = 1;

const int RAND_MAX = 32768;


/* RAND_MAX assumed to be 32767 */
int rand(void) {
    next = next * 1103515245 + 12345; /* x(n+1) = a*x(n) + m */
    return((unsigned)(next/65536) % 32768);
}

float rand_0_1() {
    int r = rand();
    float rf = (float)r / RAND_MAX;
    return rf;
}

void srand(unsigned seed) {
    next = seed;
}


int main(int argc, char** argv) {
    unsigned int hist[10];

    srand(42);

    for (int i = 0; i<10; i++) {
        hist[i] = 0;
    }

    int N = 1000;
    for (int i = 0; i<N; i++) {
        int v = rand() % 10;
        hist[v]++;
    }
    
    float avg = (float)N / 10;
    float var = 0;
    for (int i = 0; i<10; i++) {
        printf("[%d]: %d\n", i, hist[i]);
        
        int diff = hist[i] - avg;
        var += diff*diff;
    }
    float std = sqrtf(var/10);
    printf("mean = %f, std = %f\n", avg, std);

    printf("\n\n");

    printf("random num: %f\n", rand_0_1());
    printf("random num: %f\n", rand_0_1());
    printf("random num: %f\n", rand_0_1());

    return 0;
}