clc; clear; close all;

x = 0:0.01:2*pi;
y = sin(x);

h = 0.3;

% x_0 = 2.0;
% xm1 = x_0 - h;
% xp1 = x_0 + h;

xm1 = 0;
x_0 = pi/8;
xp1 = pi/4;

h = pi/8;

xs = [xm1, x_0, xp1];
ys = sin(xs);

plot(x, y); hold on;
line([0, x(length(x))], [0, 0]);
stem(xs, ys);


%%
coeff = [
    [1, 1, 0, h],
    [1/2, 1, 1/2, h],
    [1/3, 4/3, 1/3, h],
    [0, -1, 1, 1/h],
    [-1, 1, 0, 1/h],
    [-1, 0, 1, 1/(2*h)],
    [1, -2, 1, 1/(h*h)],
];

for k=1:size(coeff, 1)
    a = coeff(k, 1);
    b = coeff(k, 2);
    c = coeff(k, 3);
    m = coeff(k, 4);

    disp(num2str(a) + ", " + num2str(b)  + ", " + num2str(c) + " *" + num2str(m));
    A = (a*ys(1) + b*ys(2) + c*ys(3)) * m
end

dok = cos(x_0)