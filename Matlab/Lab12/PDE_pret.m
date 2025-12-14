
% PDE_pret.m
clear all; close all;

N=9; Tp=20; Tk=-20;
D = diag( -2*ones(N,1),0 ) + diag(ones(N-1,1),1) + diag(ones(N-1,1),-1);
b = zeros(N,1); b(1) = -Tp; b(N) = -Tk;
D, pause
b, pause

T = D \ b;
plot([Tp; T; Tk],'bo-');
xlabel('punkty x'); ylabel('temperatura [oC]'); title('Temp(x) [oC]'); grid;
