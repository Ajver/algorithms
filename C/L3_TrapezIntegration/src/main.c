#include <stdio.h>

#include "function.h"
#include "integrate.h"

int main() {
    double a, b;
    unsigned int count;

    printf("Podaj przedział [a, b]: ");
    scanf("%lf", &a);
    scanf("%lf", &b);

    printf("Podaj liczbę przedziałów: ");
    scanf("%u", &count);

    printf("Wybierz funkcję do całkowania:\n");
    printf("1. f(x) = x^2 + 3x + 2\n");
    printf("2. f(x) = sin(x)\n");
    printf("3. f(x) = e^x\n");
    printf("4. f(x) = 1 / (x + 1)\n");

    int choice;
    printf("Twój wybór: ");
	scanf("%d", &choice);

	double result = 0.0;

	switch (choice) {
		case 1:
		    result = integrate(a, b, count, f1);
		    break;
		case 2:
			result = integrate(a, b, count, f2);
			break;
		case 3:
			result = integrate(a, b, count, f3);
			break;
		case 4:
			result = integrate(a, b, count, f4);
			break;
		default:
		    printf("Nieznany wybór: %d", choice);
	}

    printf("Wynik całkowania: %f\n", result);

    return 0;
}