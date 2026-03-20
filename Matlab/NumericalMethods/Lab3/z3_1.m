u=[1;2;3]; 
v=[4;5;6];

A=[1,2,3; 4,5,6; 7,8,9]; 
B=eye(3);

%% Dodawanie elementów
disp("Dodawanie elementów")
u+v

%% Mnożenie elementów 
disp("Mnożenie elementów")
u.*v

%% Mnożenie przez liczbę
disp("Mnożenie przez liczbę")
8*u

%% Mnożenie macierzy
disp("Mnożenie macierzy")
A * u
% [ 1*1 + 2*2 + 3*3 = 14 ]
% [ 4*1 + 5*2 + 6*3 = 32 ]
% [ 7*1 + 8*2 + 9*3 = 50 ]

%% Transponowanie
disp("Transponowanie")
A.'

%% Podnoszenie do potegi
disp("Podnoszenie do potegi")
u.^v
% [ 1^4, 2^5, 3^6 ]

%% sum
disp("sum")
sum(u)

%%
disp("suma kumulowana")
cumsum(u)

