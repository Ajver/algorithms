% evd_power.m
clc; clear all; close all;

if(1) A = [ 4 0.5; 0.5 4 ];       % wybor/definicja symetrycznej macierzy kwadratowej
else  A = magic(4);
end
[ N, N ] = size(A);               % wymiar 

x = ones(N,1);                    % inicjalizacja
for i = 1:20                      % poczatek petli
    y = A*x;                      % pierwsze mnozenie
    [ymax,imax] = max(abs(y));    % najwieksza wartosc abs() i jej indeks

    % ymax_non_abs = y(imax)
    % y
    x = y/ymax;                   % wektor wlasny
    lambda = ymax;                % wartosc wlasna ymax=y(imax)
end                               % koniec petli

% X musi zostać znormalizowane do długości 1
x = x / norm(x);
% Ale co do zasady dla dowolnego wektora x, bedacego wektorem wlasny
% a*x (gdzie a jest skalarem) daje tez wektor wlasny

x, lambda,                        % pokaz wynik: max wartosc wlasna i wektor wlasny
[ V, D ] = eig(A)                 % porownaj z funkcja Matlaba
    
    
    
