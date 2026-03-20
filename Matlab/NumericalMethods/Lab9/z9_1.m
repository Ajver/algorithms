% equnonlin_balista.m
clear all; close all;

% b = @(v) 0.1*v;
b = 0.35;

m=5; 
v0=50; 
alpha=deg2rad(30); 
h=50; 
g=9.81;

x = 0 : 1 : 350;
% x = 320 : 0.001 : 330;

nawias1 = (tan(alpha) + m*g/(b*v0*cos(alpha))) * x;
nawias2 = (g*(m^2)/(b^2)) * log(1 - (x*b/(m*v0*cos(alpha))));
y = h + nawias1 + nawias2;

figure; plot(x,y); xlabel('x'); ylabel('y'); title('y(x)'); grid;


