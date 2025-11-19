% Element algorytmu Jacobiego - pojedyncza rotacja zerujaca jeden element macierzy
clear all; close all;

  A = [ 2 0 1; 0 -2 0; 1 0 2 ],    % przykład z Yang, 2005
% A = hankel( [1 2 3], [3,4,5] ),
[N,N] = size(A),

% Pojedyncza rotacja zerująca element A(p,q) macierzy A
p=1; q=3;
xi = (A(q,q)-A(p,p)) / (2*A(p,q));
if( xi > -eps ) t =  (abs(xi) + sqrt(1+xi^2));
else            t = -(abs(xi) + sqrt(1+xi^2));
end
c = 1 / sqrt(1+t^2),
s = t * c,
R1 = eye(N);
R1(p,p) =  c; R1(q,q) = c;
R1(p,q) = -s; R1(q,p) = s;
R1,
A = R1.' * A * R1,