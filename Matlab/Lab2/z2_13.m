clc; clear; close all;


a = 10;
b = 40;
c = 10;

delta = b^2 - 4*a*c
delta_sqrt = sqrt(delta)

double_a = a*2

x1 = (-b - delta_sqrt)/double_a
x2 = (-b + delta_sqrt)/double_a

if abs(x1) > abs(x2)
    x1_2 = x1
    x2_2 = (2*c)/((-b - delta_sqrt))
else
    x1_2 = (2*c)/((-b + delta_sqrt))
    x2_2 = x2
end

err_1 = x1_2 - x1
err_2 = x2_2 - x2



