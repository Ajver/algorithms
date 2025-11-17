/*
To run:
gcc psum.c -o psum -lm && ./psum 3 4 4
*/

#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

typedef struct {
    int* arr;
    int low;
    int high;
} ThreadSummingArgs;

int sum_subarray(int* a, int low, int high) {
    int sum = 0;
    for (int i = low; i < high; i++) {
        sum += a[i];
    }
    return sum;
}


void* thread_summing(void* any_args) {
    ThreadSummingArgs* args = any_args;

    int* result = malloc(sizeof(int));
    *result = sum_subarray(args->arr, args->low, args->high);

    printf("sum[%d:%d]: %d\n", args->low, args->high, *result);

    free(args);
    return result;
}

int min(int a, int b) {
    return a < b ? a : b;
}

void print_arr(int* arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("[%d] = %d\n", i, arr[i]);
    }
}


int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Please specify 3 parameters: n, k, t");
        return 1;
    }

    int n = atoi(argv[1]);
    int k = atoi(argv[2]);
    int t = atoi(argv[3]);
    
    int tab_len = n * k;

    printf("Creating %dx%d table, summing using %d threads\n", n, k, t);

    // 1D array, with n*k elements
    int* table = (int*)malloc(tab_len * sizeof(int));

    for (int i = 0; i < tab_len; i++) {
        table[i] = rand() % 10;
    }

    print_arr(table, tab_len);

    int sum = sum_subarray(table, 0, tab_len);
    printf("\nSum: %d\n", sum);

    pthread_t* threads = (pthread_t*)malloc(t * sizeof(pthread_t));
    int* k_sums = (int*)malloc(k * sizeof(int));

    int k_sums_offset;
    int total_iterations_left = k;
    for (int epoch = 0; epoch < ceil((float)k / t); epoch++) {
        int iters_this_epoch = min(total_iterations_left, t);
        int idx_offset = epoch*t;

        for (int i = 0; i < iters_this_epoch; i++) {
            int idx = idx_offset + i;

            ThreadSummingArgs* args = malloc(sizeof *args);
            args->arr = table;
            args->low = idx * n;
            args->high = args->low + n;
            pthread_create(&threads[i], NULL, thread_summing, args);
        }
        
        for (int i = 0; i < iters_this_epoch; i++) {
            // This loop is executted up to k times. 
            // Each epoch solves t sums, but t may be < than k, so we need another epoch.
            
            int* result;
            int idx = idx_offset + i;
            pthread_join(threads[i], (void**)&result);
            k_sums[idx] = *result;
        }

        total_iterations_left -= iters_this_epoch;
    }

    printf("-------------\n\nk sums:\n");
    print_arr(k_sums, k);

    int sum_of_subs = sum_subarray(k_sums, 0, k);
    printf("Sum of subs: %d\n", sum_of_subs);

    free(threads);
    free(table);

    return 0;
}