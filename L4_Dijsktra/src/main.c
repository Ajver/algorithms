#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


/*

5 0 10 0 30 0 10 0 50 0 0 0 50 0 0 20 30 0 0 0 60 0 0 20 60 0 0

*/


int* dijkstra(int startingNode, int nodesCount, int** graph) {
    int* dFromSource = malloc(nodesCount * sizeof(int));
    bool* visitedNodes = malloc(nodesCount * sizeof(bool));

    for (int i=0; i<nodesCount; i++) {
        // -1 is "INFINITE" (not yet calculated) value
        dFromSource[i] = -1;
        visitedNodes[i] = false;
    }
    dFromSource[startingNode] = 0;
    visitedNodes[startingNode] = true;

    for (int i=0; i<nodesCount; i++) {
        int cost = graph[startingNode][i];
        if (cost <= 0) {
            // No connection to this node from the currentNode
            continue;
        }

        dFromSource[i] = cost;
    }

    int smallestCost = -1;
    for (int i=0; i<nodesCount; i++) {
        if (visitedNodes[i]) {
            // Already visited
            continue;
        }
        // if (smallestCost == -1 || dFromSource[i] < )
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

    printf("Podaj liczbe wierzcholkow w grafie: ");
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

    printGraph(nodesCount, graph);

    printf("Podaj wierzcholek poczatkowy: ");
    scanf("%d", &startingNode);

    int* dFromSource = dijkstra(startingNode, nodesCount, graph);

    printf("Wierzchołek\tOdległość od startu\n");
    for (int i=0; i<nodesCount; i++) {
        printf("%d\t\t%d\n", i, dFromSource[i]);
    }

    for (int i=0; i<nodesCount; i++) {
        free(graph[i]);
    }
    free(graph);

    return 0;
}