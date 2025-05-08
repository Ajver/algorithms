#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#define SIZE 6
#define INF 99999999


void printGraph(int graph[][SIZE]) {
	for (int y=0; y<SIZE; y++) {
		for (int x=0; x<SIZE; x++) {
			printf("%d ", graph[y][x]);
		}
		printf("\n");
 	}
}

int find_lowest(int set[], int mask[], size_t size) {
	int idx = -1;
	int smallest = INF;

	for (int i=0; i<size; i++) {
		if (!mask[i]) {
			continue;
		}

		if (set[i] < smallest) {
			smallest = set[i];
			idx = i;
		}
	}

	return idx;
}

void print_list(int list[], size_t size) {
	for (int i=0; i<size; i++) {
		printf("%d ", list[i]);
	}
	printf("\n");
}

void printPathBackwards(int previousNodes[], int currentNode, int startingNode) {
	if (currentNode == startingNode) {
		return;
	}

	printPathBackwards(previousNodes, previousNodes[currentNode], startingNode);

	printf("%d ", previousNodes[currentNode]);
}


void astar(int graph[][SIZE], int* h_cost, int startingNode, int endingNode) {
	int open[SIZE] = {false, false, false, false, false, false};
	int closed[SIZE] = {false, false, false, false, false, false};
	open[startingNode] = true;

	int f_cost[SIZE] = {INF, INF, INF, INF, INF, INF};
	f_cost[startingNode] = 0;

	int previousNodes[SIZE] = {-1, -1, -1, -1, -1, -1};

	while (true) {
		int current = find_lowest(f_cost, open, SIZE);
		open[current] = false;
		closed[current] = true;

		// printf("current: %d\n", current);

		if (current == endingNode) {
			// print_list(previousNodes, SIZE);

			printf("Najkrótsza ścieżka: ");
			printPathBackwards(previousNodes, endingNode, startingNode);
			printf("%d\n", endingNode);
			printf("Całkowity koszt: %d", f_cost[endingNode]);

			return;
		}

		for (int i=0; i<SIZE; i++) {
			int cost = graph[current][i];
			if (closed[i] || cost <= 0) {
				continue;
			}

			// printf("Neighbour: %d\n", i);

			int new_cost = f_cost[current] + cost;

			if (new_cost < f_cost[i] || !open[i]) {
				f_cost[i] = new_cost;
				previousNodes[i] = current;
				open[i] = true;
			}
		}
	}
}


int main(int argc, const char * argv[]) {
	int heuristics[SIZE] = {5, 3, 4, 2, 6, 0};
	int graph[SIZE][SIZE] = {
		0, 1, 0, 0, 0, 10,
		0, 0, 2, 1, 0, 0,
		0, 0, 0, 0, 5, 0,
		0, 0, 0, 0, 3, 4,
		0, 0, 0, 0, 0, 2,
		0, 0, 0, 0, 0, 0
	};

	int startingNode = 0;
	int	endingNode = 5;

	printf("\nPodaj heurystyki dla każdego węzła:\n");
	for (int i=0; i<SIZE; i++) {
		printf("h(%d) = \n", i);
		scanf("%d", &heuristics[i]);
	}

	printf("Podaj koszty krawędzi (macierz 6x6, 0 oznacza brak krawędzi):\n");
	for (int y=0; y<SIZE; y++) {
		for (int x=0; x<SIZE; x++) {
			scanf("%d", &graph[y][x]);
		}
	}

	printf("Podaj węzeł startowy i docelowy: \n");
	scanf("%d", &startingNode);
	scanf("%d", &endingNode);

	// printGraph(graph);
	astar(graph, heuristics, startingNode, endingNode);


	return 0;
}