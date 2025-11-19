% evd_qr.
clc; clear all; close all;

if(0) A = [
    16     2     3    13;
     5    11     10     8;
     9     7     6.1    12;
     4    14    15     1
    ];   % analizowana macierz
else  A = hilb(5)
end
[N,N]=size(A);                 % jej wymiary
x = ones(N,1);                 % inicjalizacja

det_A = det(A),

[Q,R] = qr(A);                 % pierwsza dekompozycja QR
for i=1:30                     % petla - start
    [Q,R] = qr(R*Q);           % kolejne iteracje
end                            % petla -stop
A1 = R*Q,                      % ostatni wynik
lambda = sort(diag(A1)),             % elementy na przekatnej
ref = sort(eig(A)),                  % porownanie z Matlabem
