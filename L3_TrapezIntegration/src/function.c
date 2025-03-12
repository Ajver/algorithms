#include <math.h>
#include "function.h"

double f1(double x) {
  // f(x) = x^2 + 3x + 2
  return x*x + 3.0*x + 2.0;
}

double f2(double x) {
  // f(x) = sin(x)
  return sin(x);
}

double f3(double x) {
  // f(x) = e^x
  return exp(x);
}

double f4(double x) {
  // f(x) = 1 / (x + 1)
  return 1.0/(x + 1);
}
