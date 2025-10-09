clc; clear all; close all;

epsi = 0.01;

b = [1; 1];

a_range = -1:0.1:1
xs_dep_a = zeros(2, length(a_range))

TRIES = 10;

for k=1:length(a_range)

    a = a_range(k)
    
    xs_rand = zeros(2, TRIES)

    for m=1:TRIES
        A = [1, 1; a, 1];
        A = A + epsi*randn(2,2)
        
        x = inv(A)*b
        x = x.'
    
        xs_rand(:, m) = x
    end

    xs_rand
    mean_x = mean(xs_rand, 2)

    xs_dep_a(:, k) = mean_x

end

figure();

xs_dep_a(1)

subplot(2, 1, 1);
scatter(a_range, xs_dep_a(1));
title("x1")

subplot(2, 1, 2);
scatter(a_range, xs_dep_a(2));
title("x2")