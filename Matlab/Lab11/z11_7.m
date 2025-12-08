clc; clear; close all;

% https://pl.wikipedia.org/wiki/Ruch_harmoniczny
b = 0.7;  % wsp. tlumienia
f = 1;
omega = 2*pi*f;
omega_sqr = omega^2;
x = @(t, x_n) [x_n(2); -omega_sqr*x_n(1) - b*x_n(2)];

tminmax = [0, 4];
x0 = [1; 0];

[t, y] = odeEuler(x, tminmax, x0, 1e6);

subplot(2, 1, 1);
plot(t, y(:, 1), "r-");
ylabel("x(t)");

subplot(2, 1, 2);
plot(t, y(:, 2), "r-");
ylabel("v(t)");