% PDE_dyfuzja.m
% Dyfuzja ciepła w długim pręcie (w aluminiowym mieszadle zanurzonym we wrzątku)
clear all; close all;

A = 10;         % wartość skoku wielkości u(t,x)
u0 = 0;         % poziom dyfundującej wielkości u(t,x) w otoczeniu
D  = 1e-4;      % wsp. dyfuzyjności
a  = 1e-4;      % wsp. strat do otoczenia

t = 0 : 1 : 1000;  % czas
x = 0 : 0.05 : 1;
[T,X] = meshgrid(t,x);
u = A/2*( exp( -X*sqrt(a/D) ) .* erfc( X./(2*sqrt(D*T)) - sqrt(a*T) ) + ...
          exp(  X*sqrt(a/D) ) .* erfc( X./(2*sqrt(D*T)) + sqrt(a*T) ) );
      
figure; mesh( t, x, u ); xlabel('t [s]'); ylabel('x [m]'); title('u(t,x)'); pause

% Kino
px = 0.7*max(x);
py = 0.9*max(max(u));
figure;
for iter = 1 : length( t )
  % iter
    plot( x, u(:,iter) ), xlabel('x [m]'); title('temp(x)'); grid;
    text( px,py,['czas = ' num2str( t(iter) ) '[sec]']);
    pause(0.005)
end 