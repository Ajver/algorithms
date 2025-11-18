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
    int start_idx;
    int end_idx;
} ThreadSummingArgs;

int sum_subarray(int* a, int start_idx, int end_idx) {
    // Sums elements from a, from start_idx to end_idx EXCLUDING!
    // [ start_idx, end_idx )
    int sum = 0;
    for (int i = start_idx; i < end_idx; i++) {
        sum += a[i];
    }
    return sum;
}


void* thread_summing(void* any_args) {
    ThreadSummingArgs* args = any_args;

    int* result = malloc(sizeof(int));
    *result = sum_subarray(args->arr, args->start_idx, args->end_idx);

    printf("sum[%d:%d]: %d\n", args->start_idx, args->end_idx, *result);

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

    // Buffer of t threads batch. When t < k, the threads are re-used in next epochs,
    // in order to calculate the whole array.
    pthread_t* threads = (pthread_t*)malloc(t * sizeof(pthread_t));

    int* k_sums = (int*)malloc(k * sizeof(int));

    int k_sums_offset;
    int total_iterations_left = k;
    for (int epoch = 0; epoch < ceil((float)k / t); epoch++) {
        int iters_this_epoch = min(total_iterations_left, t);
        int idx_offset = epoch*t;

        for (int i = 0; i < iters_this_epoch; i++) {
            int subarr_idx = idx_offset + i;

            ThreadSummingArgs* args = malloc(sizeof *args);
            args->arr = table;
            args->start_idx = subarr_idx * n;
            args->end_idx = args->start_idx + n;
            pthread_create(&threads[i], NULL, thread_summing, args);
        }
        
        for (int i = 0; i < iters_this_epoch; i++) {
            // This loop is executted up to k times. 
            // Each epoch solves t sums, but t may be < than k, so we need another epoch to calculate the rest
            
            int* result;
            pthread_join(threads[i], (void**)&result);

            int subarr_idx = idx_offset + i;
            k_sums[subarr_idx] = *result;
            free(result);
        }

        total_iterations_left -= iters_this_epoch;
    }

    printf("-------------\n\nk sums:\n");
    print_arr(k_sums, k);

    int sum_of_subs = sum_subarray(k_sums, 0, k);
    printf("Sum of subs: %d\n", sum_of_subs);

    free(threads);
    free(k_sums);
    free(table);

    return 0;
}