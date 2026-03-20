% PDE_dyfuzja_num.m
  clear all; close all;

  D = 0.0001;                    % stała dyfuzji  
  Tp = 20;                       % temperatura początkowa po lewej stronie
  xmax = 2;                      % długość pręta
  nx = 100;                      % liczba punktów przestrzennych
  dx = xmax/nx;                  % krok w przestrzeni
  tmax = 100;                    % czas obserwacji
  nt = 100;                      % liczba punktów czasowych
  dt = tmax/nt;                  % krok w czasie
  q = (D*dt)/dx^2;               % stała w równaniu, teraz 0.4
  u0 = zeros(1,nx); u0(1) = Tp;  % warunek początkowy wzdłuż pręta dla t=0
  U = u0;                        % zapamiętanie poprzedniej chwili
% Iteracyjne rozwiązanie równania różniczkowego
  for n = 1 : nt-1               % PO CZASIE
      u1(1) = Tp;                % punkt 1 w przestrzeni dla następnej chwili
      for j = 2 : nx-1           % W PRZESTRZENI - kolejne punkty w przestrzeni
             u1(j) =  u0(j)  + q  *( u0(j+1) - 2*u0(j) + u0(j-1) );  % (11.29)
      end % (nowe) = (stare) + wsp*( stara druga pochodna )
      u1(nx) = u0(nx) + q*( 2*u0(nx-1) - 2*u0(nx) );   % punkt ostatni (11.33)
      U = [U; u1];               % zapamiętaj obecne rozwiązanie
      u0 = u1;                   % aktualizacja bufora: obecne --> poprzednie
  end
  x = 0 : dx : xmax-dx; t = 0 : dt : tmax-dt;
  figure; mesh(x,t,U); grid; xlabel('x [m]'); ylabel('t [s]'); title('U(x,t)'); pause

