clc; clear; close all;

global wybor;
wybor = "2";

function yfun = fun(xin)
global wybor;
    switch wybor
        case "sin"
            yfun = sin(xin);
        case "2"
            yfun = polyval([2, 1, 1/2], xin);
        case "3"
            yfun = polyval([3, 2, 1, 1/2], xin);
    end
end


function yfun = funPoch(xin)
global wybor;
    switch wybor
        case "sin"
            yfun = cos(xin);
        case "2"
            yfun = polyval([4, 1], xin);
        case "3"
            yfun = polyval([9, 4, 1], xin);
    end
end

x = 0:0.01:2*pi;
y = fun(x);

h = pi/4;

xm1 = 0;
x_0 = pi/4;
xp1 = pi/2;

xs = [xm1, x_0, xp1];
ys = fun(xs);

plot(x, y); hold on;
line([0, x(length(x))], [0, 0]);
stem(xs, ys);


%%
coeff = [
    [-3, 4, -1, 1/(2*h)],
    [-1, 0, 1, 1/(2*h)],
    [1, -4, 3, 1/(2*h)],
];

for k=1:size(coeff, 1)
    a = coeff(k, 1);
    b = coeff(k, 2);
    c = coeff(k, 3);
    m = coeff(k, 4);

    disp("p'(x_" + num2str(k) + "): " + num2str(a) + ", " + num2str(b)  + ", " + num2str(c) + " *" + num2str(m));
    poch(k) = (a*ys(1) + b*ys(2) + c*ys(3)) * m
end

err = poch - funPoch(xs)

powers = (length(xs)-1):-1:0;
for r=1:length(xs)
    for c=1:length(xs)
        X(r, c) = xs(r)^powers(c);
    end
end

a = inv(X) * (ys')
test = polyfit(xs, ys, length(xs)-1)'

plot(x, polyval(a, x));


