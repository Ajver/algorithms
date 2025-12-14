% PDE_dyfuzja_num.m
clear all; close all;

D = 0.0001;                    % stała dyfuzji  
Tp = 20;                       % temperatura początkowa po lewej stronie
xmax = 2;                      % długość pręta
nx = 40;                      % liczba punktów przestrzennych
dx = xmax/nx;                  % krok w przestrzeni
tmax = 1000;                    % czas obserwacji
nt = 1000;                      % liczba punktów czasowych
dt = tmax/nt;                  % krok w czasie
q = (D*dt)/dx^2               % stała w równaniu
u0 = zeros(nx, 1); u0(1) = Tp;  % warunek początkowy wzdłuż pręta dla t=0
U = u0';                        % zapamiętanie poprzedniej chwili

czy_zbierzne = q < 0.5

% Wspolczynniki
C = (1 - 2*q)*eye(nx) + diag(q*ones(nx-1,1), 1) + diag(q*ones(nx-1,1), -1);
C(1, :) = zeros(1, nx); C(1, 1) = 1;
C(nx, nx-1) = 2*q;

for j = 1 : nt-1               % PO CZASIE
  u1 = C*u0;
  
  U = [U; u1'];               % zapamiętaj obecne rozwiązanie
  u0 = u1;                   % aktualizacja bufora: obecne --> poprzednie
end
x = 0 : dx : xmax-dx; t = 0 : dt : tmax-dt;
figure; mesh(x,t,U); grid; xlabel('x [m]'); ylabel('t [s]'); title('U(x,t)');

