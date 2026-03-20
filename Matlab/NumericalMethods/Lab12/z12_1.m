% PDE_przyklad.m - pierwszy przykład
% d^2[f(x)]                                  df(x)|
% -------- = 1,  0 <= x <= 4, f(x=1)=-1/2;  ------|    =1
%   d^2[x]                                    dx  | x=3

clear all; close all;

% Równania drugich pochodnych w punktach
  A = [  1,  1,  0,  0; ...    % punkt x0
         0, -2,  1,  0; ...    % punkt x2
         0,  1, -2,  1; ...    % punkt x3 
         0,  2,  0, -2 ];      % punkt x4
% Wektor po prawej stronie
  b = [ 0; ...
        1.5; ...
        1; ...
       -4 ];
% Rozwiązanie numeryczne
  fnum = A \ b;
  
% Porównanie z rozwiązaniem analitycznym f(x) = 0.5*(x-2)^2 + 1
  x = 0 : 0.01 : 4;           % zmienność argumentu
  f = 0.5*(x-2).^2 - 1;       % funkcja
  fd = (x-2);                 % jej pierwsza pochodna
  fdd = 1*ones(1,length(x));  % jej druga pochodna

  xfdd = [0, 2, 3, 4]';
  
  x0=1; f0=-1/2; xd0=3; fd0=1;
  plot(x,f,'w-', 'Linewidth',2,'MarkerSize',7); hold on; grid on;
  plot(x,fd,'b--', 'Linewidth',2,'MarkerSize',7); 
  plot(x,fdd,'r:', 'Linewidth',2,'MarkerSize',7); 
  plot(xfdd,fnum,'mo', 'Linewidth',2,'MarkerSize',7); 
  plot(x0,f0,'ks', 'Linewidth',2,'MarkerSize',7); 
  plot(xd0,fd0,'b^', 'Linewidth',2,'MarkerSize',7); 
  
  xlabel('x'); title('Funkcja f(x) i jej pochodne');
  legend('funkcja f(x)', '1-sza pochodna', '2-druga pochodna', ...
         'Obliczone','Warunek f(1)','Warunek fd(3)','Location','north');
  axis([0,4,-2,3]);
