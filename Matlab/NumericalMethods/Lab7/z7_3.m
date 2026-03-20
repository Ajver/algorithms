clc; clear; close all;

N = 1000;
h = 2*pi/N;
t = (0:N-1) * h;

clean_x = sin(t);
epsilon = 0.1;
x = clean_x + epsilon*randn(1, N);

plot(t, x); hold on;
plot(t, clean_x);
legend(["x noisy", "x clean"]);
title("Noisy x(t) = sin(t) + \epsilon")

d1_true = cos(t);
d2_true = -sin(t);

k_range = 2:2:500;

for k=k_range
    d1 = (x(1+k:N)-x(1:N-k))/(h*k);
    d1_MAE(k/2) = mean(abs(d1 - d1_true(1+k/2:N-k/2)));
    
    d2 = (x(1:N-k) -2*x(1+k/2:N-k/2) + x(1+k:N))/((h*k/2)^2);
    d2_MAE(k/2) = mean(abs(d2 - d2_true(1+k/2:N-k/2)));
end

[min_MAE1, best_MAE1_idx] = min(d1_MAE);
[min_MAE2, best_MAE2_idx] = min(d2_MAE);
% *2 because MAE arrays are indexed using every second k
best_k1 = best_MAE1_idx*2;
best_k2 = best_MAE2_idx*2;
fprintf("best k for d1 = %d\n", best_k1);
fprintf("best k for d2 = %d\n", best_k2);

figure;
subplot(2, 1, 1);
plot(k_range, d1_MAE);
xline(best_k1, "y--");
yscale("log");
title("MAE for d1");
xlabel("k");
ylabel("avg |num x' - true x'|");
legend("MAE for each k", "best k = " + num2str(best_k1));

subplot(2, 1, 2);

plot(k_range, d2_MAE);
xline(best_k2, "y--");
yscale("log");
title("MAE for d2");
xlabel("k");
ylabel("avg |num x'' - true x''|");
legend("MAE for each k", "best k = " + num2str(best_k2));


figure;
subplot(2, 1, 1);

k = best_k1;
d1 = (x(1+k:N)-x(1:N-k))/(h*k);
plot(t(1+k/2:N-k/2), d1); hold on;

plot(t, d1_true);
legend(["num dx/dt", "true dx/dt"]);
title("dx/dt numerical using k = " + num2str(k));

subplot(2, 1, 2);
k = best_k2;
d2 = (x(1:N-k) -2*x(1+k/2:N-k/2) + x(1+k:N))/((h*k/2)^2);
plot(t(1+k/2:N-k/2), d2); hold on;

plot(t, d2_true); 
legend(["num d^2x/dt^2", "true d^2x/dt^2"]);
title("d^2x/dt^2 numerical using k = " + num2str(k));


M = 1;
h_opt_d1 = (3*epsilon / M)^(1/3)
h_opt_d2 = (48*epsilon / M)^(1/4)

% 2* because k in this algorithm is double the step between central point
% and surroundings
theoretical_k_opt_d1 = 2* round(h_opt_d1/h)
theoretical_k_opt_d2 = 2* round(h_opt_d2/h)
