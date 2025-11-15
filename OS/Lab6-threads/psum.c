/*
To run:
gcc psum.c -o psum && ./psum 3 4 4
*/

#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


int sum_subarray(int a[], int low, int high) {
    int sum = 0;
    for (int i = low; i < high; i++) {
        sum += a[i];
    }
    return sum;
}


int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Please specify 3 parameters: n, k, t");
        return 1;
    }

//    srand(time(NULL));

    int n = atoi(argv[1]);
    int k = atoi(argv[2]);
    int tab_len = n * k;

    int t = atoi(argv[3]);

    printf("Creating %dx%d table, summing using %d threads\n", n, k, t);

    // 1D array, with n*k elements
    int* table = (int*)malloc(tab_len * sizeof(int));

    for (int i = 0; i < tab_len; i++) {
        table[i] = rand() % 10;
        printf("%d > %d\n", i, table[i]);
    }

    int sum = sum_subarray(table, 0, tab_len);
    printf("Sum: %d\n", sum);

    int* k_sums = (int*)malloc(k * sizeof(int));
    for (int i = 0; i < k; i++) {
        //pthread_t thread;
        //pthread_create(&thread1, NULL, foo, NULL);
        k_sums[i] = sum;
    }

    free(table);

    return 0;
}