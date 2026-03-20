% interp_lagrange.m
clc; clear all; close all;

% temperatura w Krakowie
x = [ 6,  7,  8,    9,  10,   11, 11.5, 12, 12.25 ]; 
y = [ 15, 16, 16.5, 17, 17.5, 18, 20,   21  22 ];  
xi = [5.8: 1/12 : 13];

[yi,a] = funTZ_lagrange(x,y,xi);  % nasza funkcja interpolujaca
yii = polyval(a,xi);               % oblicz wartosci wielomianu "a" w punktach "xi" 
a,                                 % obliczone wsp. wielomianu: aN,...,a1,a0
figure; plot(x,y,'ro',xi,yi,'b-',xi,yii,'k-'); title('y=f(x)');   % rysunek
hold on;

% Ogólnie liczba punktów poprawia jakość interpolacji w [xmin, xmax]
% ale pogarsza jakość extrapolacji