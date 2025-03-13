#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "game_of_life.h"

int max(int a, int b) {
	return a > b ? a : b;
}

int min(int a, int b) {
	return a < b ? a : b;
}

unsigned int count_neighbours(bool** tab, int w, int h, int cx, int cy) {
	unsigned int count = 0;

	for (int y = max(cy-1, 0); y <= min(cy+1, h-1); y++) {
		for (int x = max(cx-1, 0); x <= min(cx+1, w-1); x++) {
			if (x == cx && y == cy) {
				// It's THIS cell - ignore it!
				continue;
			}
			if (tab[x][y]) {
				count++;
			}
		}
	}

	return count;
}

void simulate(bool** tab, int w, int h) {
	bool** tab_next_gen;
	tab_next_gen = malloc(w * h * sizeof(bool));
	for (int i = 0; i < w; i++) {
		tab_next_gen[i] = malloc(h * sizeof(bool));
	}

	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {
			unsigned int neighbours = count_neighbours(tab, w, h, x, y);

			if (tab[x][y]) {
				// Alive!
				if (neighbours == 2 || neighbours == 3) {
					 tab_next_gen[x][y] = true;
				} else {
					tab_next_gen[x][y] = false;
				}
			}else {
				// Dead :c
				if (neighbours == 3) {
					tab_next_gen[x][y] = true;
				}else {
					tab_next_gen[x][y] = false;
				}
			}
		}
	}

	// Rewrite
	//	memcpy(tab, tab_next_gen, w * h * sizeof(bool));
	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {
			tab[x][y] = tab_next_gen[x][y];
		}
	}

	for (int i = 0; i < w; i++) {
		free(tab_next_gen[i]);
	}
	free(tab_next_gen);
}

void print_map(bool** tab, int w, int h) {
	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {
			printf("%s", tab[x][y] ? "O" : ".");
		}
		printf("\n");
	}
}


void fill_map_randomly(bool** tab, int w, int h, int cells_count) {
	// Clear map first
	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {
			tab[x][y] = false;
		}
	}

	for (int i = 0; i < cells_count; i++) {
		int x = rand() % w;
		int y = rand() % h;

		if (tab[x][y]) {
			// Cell is already in here
			i--;
			continue;
		}

		tab[x][y] = true;
	}
}