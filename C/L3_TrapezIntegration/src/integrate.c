#include <stdio.h>
#include "integrate.h"


double integrate(double a, double b, unsigned int count, double (*f)(double)) {
	double step = (b - a) / count;
	double result = 0.0;

	double prevY = f(a);
	for (int i = 0; i < count; i++) {
		double x = a + (i+1) * step;
		double y = f(x);
		double sum = (prevY + y) * step / 2.0;
//		printf("x = %f, y = %f, sum = %f, result = %f\n", x, y, sum, result);
		prevY = y;

		result += sum;
	}

	return result;
}