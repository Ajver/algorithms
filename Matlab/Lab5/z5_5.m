% interp_lagrange.m
clear all; close all;;

% temperatura w Krakowie
x = [ 5, 6, 8, 11 ]; y = [ -2, 3, 7, 10 ];  
xi = [4: 1/12 : 12];

[yi,a] = funTZ_lagrange(x,y,xi);  % nasza funkcja interpolujaca
%[yi,a,p] = funTZ_newton(x,y,xi);   % nasza funkcja interpolujaca
yii = polyval(a,xi);               % oblicz wartosci wielomianu "a" w punktach "xi" 
a,                                 % obliczone wsp. wielomianu: aN,...,a1,a0
figure; plot(x,y,'ro',xi,yi,'b-',xi,yii,'k-'); title('y=f(x)');   % rysunek
hold on;

x_7_15 = 7.25;
y_7_15 = polyval(a, x_7_15)  % 6.1563 *C
plot(x_7_15, y_7_15, "r*", MarkerSize=17);

y_treshold = 1;
godz_pow_threshold = xi(find(yii > y_treshold, 1));
disp("Powyzej 1 *C od godz: " + floor(godz_pow_threshold) + ":" + floor(((godz_pow_threshold-floor(godz_pow_threshold)) * 60)))
plot(xlim, [y_treshold , y_treshold ], "g-");
plot(godz_pow_threshold, y_treshold, "r*", MarkerSize=17);

%% Nowa dana
x(end+1) = 14;
y(end+1) = 14;
xi = [4 : 1/12 : 15];

[yi,a] = funTZ_lagrange(x,y,xi);  % nasza funkcja interpolujaca
yii = polyval(a,xi);               % oblicz wartosci wielomianu "a" w punktach "xi" 
figure; plot(x,y,'ro',xi,yi,'b-',xi,yii,'k-'); title('y=f(x)');   % rysunek
hold on;

disp("Po dodaniu nowej danej y(14) = 14");
x_7_15 = 7.25;
y_7_15 = polyval(a, x_7_15)  % 6.1563 *C
plot(x_7_15, y_7_15, "r*", MarkerSize=17);

y_treshold = 1;
godz_pow_threshold = xi(find(yii > y_treshold, 1));
disp("Powyzej 1 *C od godz: " + floor(godz_pow_threshold) + ":" + floor(((godz_pow_threshold-floor(godz_pow_threshold)) * 60)))
plot(xlim, [y_treshold , y_treshold ], "g-");
plot(godz_pow_threshold, y_treshold, "r*", MarkerSize=17);

