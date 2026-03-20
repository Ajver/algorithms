function [yi,a,p] = funTZ_newton(xk,yk,xi)

Nk=length(xk);   % liczba wartosci wejsciowych
Ni=length(xi);   % liczba wartosci wyjsciowych (interpolowanych)

% Ilorazy roznicowe (divided differences)
d(:,1) = yk(1:Nk);  % wstawienie wartosci do pierwszej kolumny
for k = 2 : Nk      % w kolejnych kolumnach
    for w = k : Nk  % w kolejnych wierszach na przekątnej i poniżej:
        tmp1 = d(w,k-1)-d(w-1,k-1);  % kolumna przed: element minus element powyżej
        tmp2 = xk(w)-xk(w-k+1);      % argument w-ty minus odleglosc od diag + 1
        d(w,k) =  tmp1 / tmp2;       % iloraz roznicowy
    end
end
% Wspolczynniki "w" wielomianu w zapisie Newtona
p = diag(d);

% Wartosci interpolowane
yi=[];
for i=1:Ni
    yi(i) = cumprod( [1, xi(i)-xk(1:Nk-1)] ) * p;
end

% Wspolczynniki "a" wielomianu w zapisie klasycznym
a=zeros(1,Nk); a(Nk)=p(1);
for k = 1 : Nk-1
    a = a + p(k+1) * [ zeros(1,Nk-k-1) poly(xk(1:k)) ]; 
end
