% rowlin_ar.m
clc; clear all; close all;

fpr = 10000; dt = 1/fpr;      % liczba probek danych na sekunde, okres probkowania
f = [ 999   2500  3000  ];    % liczba powtorzen na sekunde skladowych sinusoid
d = [ 3     4     5     ];    % tlumienie skladowych
A = [ 10    2     0.5   ];    % amplituda skladowych
K = length(f);                % liczba skladowych sygnalu
P = 2*K;                      % rzad predykcji: podwojona liczba skladowych
N = 2*P                       % potrzebna liczba danych
x = zeros(1,N);               % inicjalizacja danych 
for k = 1 : K                 % generacja i akumulacja kolejnych sinusoid  
    x =  x + A(k) * exp(-d(k)*(0:N-1)*dt) .* cos(2*pi*f(k)*(0:N-1)*dt + pi*rand(1,1));
end
X = toeplitz( x(P:2*P-1), x(P:-1:1) ),   % macierz Toeplitza probek danych
x = x( P+1 : P+P)',                      % wektor danych
a = inv(X)*x;                            % rozwiazanie rownania  
r = roots( [1, -a'] );                   % pierwiastki wielomianu
pow = log( r );                          % logarytm naturalny z pierwiastkow                                
omega = imag(pow);                       % czesc urojona
[omega, indx] = sort( omega, 'ascend' ); % sortowanie min-max
fest = omega(K+1:2*K)/(2*pi*dt),         % czestotliwosci skladowych (dodatnie)
dest = -real( pow(indx(K+1:2*K)) )/dt,   % tlumienie skladowych

%% Wersja z szumem

disp("=================")
disp("SZUM")

fpr = 10000; dt = 1/fpr;      % liczba probek danych na sekunde, okres probkowania
f = [ 999   2500  3000  ];    % liczba powtorzen na sekunde skladowych sinusoid
d = [ 3     4     5     ];    % tlumienie skladowych
A = [ 10    2     0.1   ];    % amplituda skladowych
K = length(f);                % liczba skladowych sygnalu
P = 2*K;                      % rzad predykcji: podwojona liczba skladowych
N = 2*P                       % potrzebna liczba danych
x = zeros(1,N);               % inicjalizacja danych 
for k = 1 : K                 % generacja i akumulacja kolejnych sinusoid  
    szum = 0.00001 * randn();
    x =  x + A(k) * exp(-d(k)*(0:N-1)*dt) .* cos(2*pi*f(k)*(0:N-1)*dt + pi*rand(1,1)) + szum;
end
X = toeplitz( x(P:2*P-1), x(P:-1:1) ),   % macierz Toeplitza probek danych
x = x( P+1 : P+P)',                      % wektor danych
a = inv(X)*x;                            % rozwiazanie rownania  
r = roots( [1, -a'] );                   % pierwiastki wielomianu
pow = log( r );                          % logarytm naturalny z pierwiastkow                                
omega = imag(pow);                       % czesc urojona
[omega, indx] = sort( omega, 'ascend' ); % sortowanie min-max
fest = omega(K+1:2*K)/(2*pi*dt),         % czestotliwosci skladowych (dodatnie)
dest = -real( pow(indx(K+1:2*K)) )/dt,   % tlumienie skladowych

fest_err = fest - f',
dest_err = dest - d';