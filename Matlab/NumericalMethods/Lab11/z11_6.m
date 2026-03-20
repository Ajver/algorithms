clc; clear; close all;

x = @(t, x_n) (4*exp(0.8*t) - 0.5*x_n);
tminmax = [0, 4];

x0 = 2;

[t, y] = odeEuler(x, tminmax, x0, 10000);

y_true = (4/1.3) * (exp(0.8*t) - exp(-0.5*t)) + 2*exp(-0.5*t);

plot(t, y_true, "b-"); hold on; grid on;
plot(t, y, "r-");
