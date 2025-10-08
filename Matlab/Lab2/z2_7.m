clc; clear; clear all;

realmin('single'), realmax('single'), eps('single'),
intmin('int8'), intmax('uint64'),




%% Wyznaczanie single

F = 0.5^23; %23 bity mantysy
E = 2^8-1; %8 Bitów Exponenty
disp("single float32 wyznaczony: " + ((1+F)*2^(E-127)));



%% UInt 64bitowy w U2
B = 2^64-1; %63 bity bo jeden ujemy
min_B=-(2^64) %Bit największy ujemny

disp("Uint 64b max: " + B);
disp("Uint 64b min: " + min_B);

%% Int8

B = 2^8-1;
disp("int8 max: " + B)