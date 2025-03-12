#include <stdio.h>
#include <stdlib.h>

#include "sort.h"


void print_tab(int* tab, int len) {
	for (int i = 0; i < len; i++) {
		printf("%d ", tab[i]);
	}
	printf("\n");
}

int main() {
	int* tab;
	int len;

	printf("Podaj rozmiar tablicy: ");
	scanf("%d", &len);

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
			quick_sort(tab, 0, len);
			break;
		case 4:
			merge_sort(tab, 0, len);
			break;
		default:
			printf("Niepoprawny wybór: %d", choice);
	}

	printf("Tablica po sortowaniu: ");
	print_tab(tab, len);

	free(tab);

    return 0;
}
