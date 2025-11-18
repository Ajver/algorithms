% Metoda Jacobiego przekształcen macierzy przez podobienstwo

clc; clear all; close all;

A = [
     2 0 0 3
     0 4 0 1
     0 0 1 0
     3 1 0 6
];
% A = [ 2 0 1; 0 -2 0; 1 0 2 ];    % przykład z Yang, 2005
[N, ~] = size(A);
symetrycznosc = A == A';
assert (sum(symetrycznosc, "all") == N^2);

[ml_V, ml_D] = eig(A);  % Matlabowe rozwiazanie

tol = 1e-4;

R = eye(N);
maxIterations = 10;
for k=1:maxIterations
    D = diag(diag(A));  % tylko glowna przekatna
    A_rest = A - D;  % A bez glownej przekatnej

    if (abs(sum(A_rest, "all")) < tol)
        k = k - 1;  % nie wykonujemy tej iteracji
        % Koniec elementow do wyzerowania (poza glowna przekatna)
        break
    else
        sum(A_rest, "all")
    end
    
    % max_wartosc to wektor najw. wartosci w kolejnych kolumnach
    % qs to wektor numerow wierszy, w ktorych wystepuje najwieksza wartosc
    [max_wartosc, qs] = max(abs(A_rest));
    [max_wartosc, p] = max(max_wartosc);  % p to idx wybranej kolumny
    q = qs(p);
    
    xi = (A(q,q)-A(p,p)) / (2*A(p,q));
    if( xi > -eps ) t =  (abs(xi) + sqrt(1+xi^2));
    else            t = -(abs(xi) + sqrt(1+xi^2));
    end
    c = 1 / sqrt(1+t^2);
    s = t * c;
    Ri = eye(N);
    Ri(p,p) =  c; Ri(q,q) = c;
    Ri(p,q) = -s; Ri(q,p) = s;
    Ri,
    A = Ri.' * A * Ri,

    R = R * Ri;

end

fprintf("koniec po iteracjach: %d\n", k);

R, A,
ml_V, ml_D,

