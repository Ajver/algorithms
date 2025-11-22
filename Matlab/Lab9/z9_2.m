% equnonlin_solve.m
clear all; close all;

it = 12;
% a  = pi-pi/4; b=pi+pi/5;  % znajdz zero funkcji y=sin(x) dla x=pi
% f  = @(x) sin(x);         % definicja funkcji
% fp = @(x) cos(x);         % definicja pochodnej funkcji
% z = pi

nachylenie_okolo = 10;

switch nachylenie_okolo
    case 10
        a = -4; b = 5;
        A = 0.15; B = 0.3; C = 0.1;  
    case 45
        a = -4; b = 1;
        A = -0.2; B = 0.5; C = 1;  
    case 80
        a = 0; b = 6;
        A = 2; B = 3; C = -3.5;  
end

f = @(x) A*x.^2+B*x+C; 
fp= @(x) 2*A*x+B;
delta = B^2 - 4*A*C;
z1 = (-B - sqrt(delta)) / (2*A);
z2 = (-B + sqrt(delta)) / (2*A);
z = z2
kat_paraboli_w_z = rad2deg(atan(fp(z)))


x = -10 : 0.01 : 10;
figure; plot( x, f(x), 'b-', x, fp(x),'r-'); grid; xlabel('x'); title('f(x), fp(x)');
legend('Funkcja','Jej pochodna');

cb = nonlinsolvers( f, fp, a, b, 'bisection', it );
cr = nonlinsolvers( f, fp, a, b, 'regula-falsi', it);
cn = nonlinsolvers( f, fp, a, b, 'newton-raphson', it);
figure; plot( 1:it,cb,'o-', 1:it,cr,'*-', 1:it,cn,'^-'); xlabel('iter'); title('c(iter)');
grid on, legend('Bisection','Regula-Falsi','Newton-Raphson');

dok = 0.001;

fprintf('Bisection it: %d\n', min(find(abs(cb - z)/pi <= dok)));
fprintf('Regula-Falsi method result: %d\n', min(find(abs(cr - z)/pi <= dok)));
fprintf('Newton-Raphson method result: %d\n', min(find(abs(cn - z)/pi <= dok)));

