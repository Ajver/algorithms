% PDE_przyklad.m - pierwszy przykład
% d^2[f(x)]                              d f(x)|
% -------- = 1,  0 <= x <= 4, f(x=0)=1;  ------|    =2
%   d^2[x]                                dx   | x=4

clear all; close all;

% Równania drugich pochodnych w punktach
  A = [ -2,  1,  0,  0; ...    % punkt x1
         1, -2,  1,  0; ...    % punkt x2
         0,  1, -2,  1; ...    % punkt x3 
         0,  0,  2, -2 ];      % punkt x4
% Wektor po prawej stronie
  b = [ 0; ...
        1; ...
        1; ...
       -3 ];
% Rozwiązanie numeryczne
  fnum = A \ b;
  
% Porównanie z rozwiązaniem analitycznym f(x) = 0.5*(x-2)^2 + 1
  x = 0 : 0.01 : 4;           % zmienność argumentu
  f = 0.5*(x-2).^2 - 1;       % funkcja
  fd = (x-2);                 % jej pierwsza pochodna
  fdd = 1*ones(1,length(x));  % jej druga pochodna
  
  x0=0; f0=1; xd0=4; fd0=2;
  plot(x,f,'k-', x,fd,'b--', x,fdd,'r:', 1:4,fnum,'mo', x0,f0,'ks', xd0,fd0,'b^', ...
      'Linewidth',2,'MarkerSize',7); grid;
  xlabel('x'); title('Funkcja f(x) i jej pochodne');
  legend('funkcja f(x)', '1-sza pochodna', '2-druga pochodna', ...
         'Obliczone','Warunek f(0)','Warunek fd(4)','Location','north');
  axis([0,4,-2,3]);
