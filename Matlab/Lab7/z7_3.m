clc; clear; close all;

N = 1000;
t = 0:N-1;
x = sin(2*pi/N * t);
x = x + 0.1*randn(1, N);

plot(t, sin(t/N * 2*pi)); hold on;
plot(t, x);

d1_true = (2*pi/N) * cos(2*pi/N * t);
d2_true = (2*pi/N)^2 * -sin(2*pi/N * t);

k_range = 2:2:N-1;

for k=k_range
    d1 = (x(1+k:N)-x(1:N-k))/k;
    d1_MAE(k/2) = mean(abs(d1 - d1_true(1:N-k)));
    
    d2 = (x(1:N-k) -2*x(1+k/2:N-k/2) + x(1+k:N))/((k/2)^2);
    d2_MAE(k/2) = mean(abs(d2 - d2_true(1:N-k)));
end

figure;
plot(k_range, d1_MAE);
title("MAE for d1");
xlabel("k");
ylabel("avg |f'_{num}(x) - f'(x)|");

figure;
plot(k_range, d2_MAE);
title("MAE for d2");
xlabel("k");
ylabel("avg |f''_{num}(x) - f''(x)|");


[min_MAE1, best_k1] = min(d1_MAE);
[min_MAE2, best_k2] = min(d2_MAE);

% best_k * 2 because we divide by two in creating the MAE arrays
fprintf("best k for d1 = %d\n", best_k1*2);
fprintf("best k for d2 = %d\n", best_k2*2);