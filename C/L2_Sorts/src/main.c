#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "sort.h"


void print_tab(int* tab, int len) {
	for (int i = 0; i < len; i++) {
		printf("%d ", tab[i]);
	}
	printf("\n");
}

bool is_sorted(int* tab, int len) {
	for (int i = 0; i < len - 1; i++) {
		if (tab[i] > tab[i + 1]) {
			return false;
		}
	}

	return true;
}

int main() {
	int* tab;
	int len;

	printf("Podaj rozmiar tablicy: ");
	scanf("%d", &len);

	if (len <= 0) {
		printf("Niepoprawny rozmiar tablicy!");
		return 1;
	}

	printf("Podaj %d elementów tablicy:\n", len);
	tab = malloc(len * sizeof(int));
	for (int i = 0; i < len; i++) {
		scanf("%d", &tab[i]);
	}

	printf("Wybierz algorytm sortowania:\n");
	printf("1 - Bubble Sort\n");
	printf("2 - Insertion Sort\n");
	printf("3 - Quick Sort\n");
	printf("4 - Merge Sort\n");
	printf("Twój wybór: ");

	int choice;
	scanf("%d", &choice);

	printf("Tablica przed sortowaniem: ");
	print_tab(tab, len);

	switch (choice) {
		case 1:
			bubble_sort(tab, len);
			break;
		case 2:
			insertion_sort(tab, len);
			break;
		case 3:
			quick_sort(tab, 0, len-1);
			break;
		case 4:
			merge_sort(tab, 0, len-1);
			break;
		default:
			printf("Niepoprawny wybór.");
			free(tab);
			return 1;
	}

	printf("Tablica po sortowaniu: ");
	print_tab(tab, len);

//	printf("Posortowana: %s\n", is_sorted(tab, len) ? "TAK" : "NIE");

	free(tab);

    return 0;
}
