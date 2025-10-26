% interp_lagrange.m
clear all; close all;

% temperatura w Krakowie
% x = [ 4.5, 5, 5.5, 8, 11, 14, 16, 17, 18 ]; y = [ 8, 10, 15, 21, 27, 32, 31, 29, 27 ];  
x = [ 4.5, 5, 5.5, 7, 8, 9.5, 11, 12.5, 14, 16, 17, 18 ]; y = [ 8, 10, 15, 17, 21, 24, 26, 27, 32, 31, 29, 28 ];  

xi = [4: 1/12 : 18];  

[yi,a,p] = funTZ_newton(x,y,xi);  % nasza funkcja interpolujaca
yii = polyval(a,xi);               % oblicz wartosci wielomianu "a" w punktach "xi" 
a,                                 % obliczone wsp. wielomianu: aN,...,a1,a0
figure; plot(x,y,'ro',xi,yi,'b-',xi,yii,'k-'); title('y=f(x)');   % rysunek
hold on;

