/*
To run:
gcc psum.c -o psum -lm && ./psum 3 4 4
*/

#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>
#include <stdarg.h>
#include <unistd.h>

const bool DEBUG_PRINT = false;

typedef struct {
    int* arr;
    int start_idx;
    int end_idx;
} ThreadSummingArgs;


void debug_printf(const char* text, ...) {
    if (!DEBUG_PRINT) {
        return;
    }

    va_list valist;
    va_start(valist, text);
    vprintf(text, valist);
    va_end(valist);
}


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

    debug_printf("sum[%d:%d]: %d\n", args->start_idx, args->end_idx, *result);

    free(args);
    return result;
}

int min(int a, int b) {
    return a < b ? a : b;
}

void print_arr(int* arr, int size) {
    if (!DEBUG_PRINT) {
        return;
    }
    
    for (int i = 0; i < size; i++) {
        printf("[%d] = %d\n", i, arr[i]);
    }
}

double create_and_sum_array(int n, int k, int t) {
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

    // clock is more precise than time
    clock_t start_time = clock();
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
    clock_t end_time = clock();

    printf("-------------\n\nk sums:\n");
    print_arr(k_sums, k);

    int sum_of_subs = sum_subarray(k_sums, 0, k);
    printf("Sum of subs: %d\n", sum_of_subs);

    double duration = ((double)end_time - start_time) / CLOCKS_PER_SEC;
    printf("t-threading summing took: %g seconds.\n", duration);

    free(threads);
    free(k_sums);
    free(table);

    return duration;
}

void append_to_csv(int n, int k, int t, double duration) {
    const char* filename = "measurements.csv";
    FILE* file;
    bool exists = access(filename, F_OK) == 0;

    file = fopen(filename, "a");

    if (file == NULL) {
        perror("Error opening or creating CSV file");
        return;
    }

    if (!exists) {
        // Write Header if file did not exist before opening
        fprintf(file, "n,k,t,duration\n");
    }

    fprintf(file, "%d,%d,%d,%g\n", n, k, t, duration);

    fclose(file);
}


int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Please specify 3 parameters: n, k, t");
        return 1;
    }

    int n = atoi(argv[1]);
    int k = atoi(argv[2]);
    int t = atoi(argv[3]);

    double duration = create_and_sum_array(n, k, t);

    append_to_csv(n, k, t, duration);

    return 0;
}