% equnonlin_solve.m
clear all; close all;

it = 12;

%%
a  = pi-pi/5; b=pi+pi/5;  % znajdz zero funkcji y=sin(x) dla x=pi
f  = @(x) sin(x);         % definicja funkcji
fp = @(x) cos(x);         % definicja pochodnej funkcji
z = pi
TOL = 0.001 * pi;  % 1 promil pi


%%
nachylenie_okolo = 45;

switch nachylenie_okolo
    case 10
        a = -1; b = 5;
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

TOL = 0.001;

%%
x = -10 : 0.01 : 10;
figure; plot( x, f(x), 'b-', x, fp(x),'r-'); grid; xlabel('x'); title('f(x), fp(x)');
legend('Funkcja','Jej pochodna');

cb = nonlinsolvers( f, fp, a, b, 'bisection', it );
cr = nonlinsolvers( f, fp, a, b, 'regula-falsi', it);
cn = nonlinsolvers( f, fp, a, b, 'newton-raphson', it);
figure;     
    plot( 1:it,cb,'o-' ); hold on;
    plot( 1:it,cr,'*-' );
    plot( 1:it,cn,'^-' );

xlabel('iter'); title('c(iter)');
grid on, legend('Bisection','Regula-Falsi','Newton-Raphson');

kiedy_zbierzne = @(preds) min(find(abs(preds - z) <= TOL));

fprintf('Bisection it: %d, result: %f, error: %f\n', kiedy_zbierzne(cb), cb(end), cb(end) - z);
fprintf('Regula-Falsi it: %d, result: %f, error: %f\n', kiedy_zbierzne(cr), cr(end), cr(end) - z);
fprintf('Newton-Raphson it: %d, result: %f, error: %f\n', kiedy_zbierzne(cn), cn(end), cn(end) - z);

