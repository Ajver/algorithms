
% PDE_pret.m
clear all; close all;

N=15; Tp=30; Tk=50;
D = diag( -2*ones(N,1),0 ) + diag(ones(N-1,1),1) + diag(ones(N-1,1),-1);
b = zeros(N,1); b(1) = -Tp; b(N) = -Tk;
D
b

T = D \ b;

X = linspace(0, 1, N+2);

plot(X, [Tp; T; Tk],'bo-');
xlabel('punkty x'); ylabel('temperatura [oC]'); title('Temp(x) [oC]'); grid;
