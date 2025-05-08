#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


#define INFINITY 999999999

/*

5 0 10 0 30 0 10 0 50 0 0 0 50 0 0 20 30 0 0 0 60 0 0 20 60 0 0

6 0 2 4 0 0 0 0 0 1 7 0 0 0 0 0 0 3 0 0 0 0 0 0 1 0 0 0 2 0 5 0 0 0 0 0 0 0

*/


int* dijkstra(int startingNode, int nodesCount, int** graph) {
    int* dFromSource = malloc(nodesCount * sizeof(int));
    bool* visitedNodes = malloc(nodesCount * sizeof(bool));

    for (int i=0; i<nodesCount; i++) {
        dFromSource[i] = INFINITY;
        visitedNodes[i] = false;
    }
    dFromSource[startingNode] = 0;
    visitedNodes[startingNode] = true;

	for (int c=0; c<nodesCount; c++) {
	    for (int i=0; i<nodesCount; i++) {
	        int cost = graph[i][startingNode];
	        if (cost <= 0) {
	            // No connection to this node from the currentNode
	            continue;
	        }

			int newCost = dFromSource[startingNode] + cost;
			if (dFromSource[i] > newCost) {
				dFromSource[i] = newCost;
			}
	    }

	    int smallestCost = -1;
	    int nextNodeIdx = -1;
	    for (int i=0; i<nodesCount; i++) {
	        if (visitedNodes[i]) {
	            // Already visited
	            continue;
	        }

			if (graph[startingNode][i] <= 0) {
				// Can't go there from startingNode
				continue;
			}

			if (smallestCost == -1 || dFromSource[i] < smallestCost) {
				smallestCost = dFromSource[i];
				nextNodeIdx = i;
			}
	    }

		if (nextNodeIdx == -1) {
			// No exits from the current source

			smallestCost = -1;
			for (int i=0; i<nodesCount; i++) {
				if (!visitedNodes[i]) {
					if (smallestCost == -1 || dFromSource[i] < smallestCost) {
						smallestCost = dFromSource[i];
						nextNodeIdx = i;
					}
				}
			}

			if (nextNodeIdx == -1) {
//				printf("No solution exists.\n");
				return dFromSource;
			}
		}

		startingNode = nextNodeIdx;
		visitedNodes[nextNodeIdx] = true;
	}

    free(visitedNodes);
    return dFromSource;
}


void printGraph(int nodesCount, int** graph) {
    for (int y=0; y<nodesCount; y++) {
        for (int x=0; x<nodesCount; x++) {
            printf("%d\t", graph[x][y]);
        }
        printf("\n");
    }
}


int main() {
    int nodesCount;
    int** graph;
    int startingNode;

    printf("Podaj liczbe wierzcholkow w grafie: \n");
    scanf("%d", &nodesCount);

    printf("Podaj macierz sasiedztwa (wagi krawedzi, 0 oznacza brak krawedzi):\n");

    graph = malloc(nodesCount * nodesCount * sizeof(int));
    for (int i=0; i<nodesCount; i++) {
        graph[i] = malloc(nodesCount * sizeof(int));
    }

    for (int y=0; y<nodesCount; y++) {
        for (int x=0; x<nodesCount; x++) {
            scanf("%d", &graph[x][y]);
        }
    }

//    printGraph(nodesCount, graph);

    printf("Podaj wierzcholek poczatkowy: \n");
    scanf("%d", &startingNode);

    int* dFromSource = dijkstra(startingNode, nodesCount, graph);

    printf("Wierzchołek\tOdległość od źródła\n");
    for (int i=0; i<nodesCount; i++) {
        printf("%d\t\t%d\n", i, dFromSource[i]);
    }

    for (int i=0; i<nodesCount; i++) {
        free(graph[i]);
    }
    free(graph);

    return 0;
}