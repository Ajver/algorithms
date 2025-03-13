#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#include "game_of_life.h"


int main(int argc, char** argv) {
	srand(time(NULL));

	const int W = 20;
	const int H = 10;
	bool** tab;

	int cells_count = 50;
	int iterations = 5;

	printf("Podaj liczbę początkowych żywych komórek: ");
	scanf("%d", &cells_count);

	printf("Podaj liczbę lat (iteracji): ");
	scanf("%d", &iterations);

	tab = malloc(W * H * sizeof(bool));
	for (int i = 0; i < W; i++) {
		tab[i] = malloc(H * sizeof(bool));
	}

	fill_map_randomly(tab, W, H, cells_count);

	printf("\nRok %d/%d:\n", 0, iterations);
	print_map(tab, W, H);

	for (int i = 0; i < iterations; i++) {
		simulate(tab, W, H);
		printf("\nRok %d/%d:\n", i+1, iterations);
		print_map(tab, W, H);
	}

	for (int i = 0; i < W; i++) {
		free(tab[i]);
	}
	free(tab);

	return 0;
}