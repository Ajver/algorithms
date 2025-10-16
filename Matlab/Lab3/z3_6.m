% rowlin_ar.m
clear all; close all;

fpr = 10000; dt = 1/fpr;      % liczba probek danych na sekunde, okres probkowania
f = [ 999   2500  3000  ];    % liczba powtorzen na sekunde skladowych sinusoid
d = [ 3     4     5     ];    % tlumienie skladowych
A = [ 10    2     0.5   ];    % amplituda skladowych
K = length(f);                % liczba skladowych sygnalu
P = 2*K;                      % rzad predykcji: podwojona liczba skladowych
N = 2*K                       % potrzebna liczba danych
x = zeros(1,N);               % inicjalizacja danych 
for k = 1 : K                 % generacja i akumulacja kolejnych sinusoid  
    x =  x + A(k) * exp(-d(k)*(0:N-1)*dt) .* cos(2*pi*f(k)*(0:N-1)*dt + pi*rand(1,1));
end

E = zeros(N, K*2);
for k=1:K
    OMk = 2*pi*f(k)*dt;     % omega
    Dk = d(k)*dt;
    for n=1:N
        E(n, k*2 - 1) = exp(i*(OMk + Dk)*n);
        E(n, k*2) = exp(-i*(OMk - Dk)*n);
    end
end

% Ec = x
% c = inv(E) * x'
c = E \ x'

% c = A/2 * e^(i*fi)
% |c| = A/2 => A = 2*|c|
A_obl = 2 * abs(c)
kat_tl = angle(c)  

% Dk = dk * dt
% dk = ??? z E?
dk = (-real(log(c))) / dt
