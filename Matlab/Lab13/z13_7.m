% oblicz_pi.m
clear all; close all;
format long;

N  = 1e9;                       % liczba strzalow
% Nk = 0;                             % liczba trafien w kolo
% for i = 1 : N                       % PETLA: kolejne strzaly                     
%     x = rand(1,1)*2.0 - 1.0;        % # kwadrat o boku 2
%     y = rand(1,1)*2.0 - 1.0;        % #
%     if(  sqrt( x*x + y*y ) <= 1.0)  % kolo o promieniu 1
%         Nk = Nk + 1;                % zwieksz liczbe trafien o 1
%     end                             %
% end                                 %
pi,                                 % dokadne  pi 
% mypi = 4.0 * Nk / N,                % obliczone pi                  

% Nk = numel( find( sqrt(xy(:,1).^2 + xy(:,2).^2) <= 1 ) );

N = 1e7;
Nk = 0;
methods = [
    "Numerical Recipes",
    % "Borland C/C++",
    % "Borland Delphi, Vurtual Pascal",
    "GNU Compiler Collection",
    "Microsoft Visual C/C++",
];
K = length(methods);

for k=1:K
    % xy = 2*rand(N,2)-1.0;
    method = methods(k);
    x = 2*rand_multadd(N, 42*k, method)-1.0;
    y = 2*rand_multadd(N, 43*k, method)-1.0;
    Nk = Nk + numel( find( x.^2 + y.^2 <= 1 ) ); 
end

mypi = 4.0 * Nk / (N*K),                % obliczone pi                  
err = mypi - pi,