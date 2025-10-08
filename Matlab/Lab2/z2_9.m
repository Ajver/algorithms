% bity_wykladnika.m
clc; clear all; close all;

% Zakomentować pausy + realmin/realmax (single)

if(1) % Metoda #1
  x=realmin('single'); n=0;         % x = wartosc najmniejsza, inicjalizacja licznika bitow
  num2bitstr( x ); %pause  % pokaz bity
  while( x < realmax('single') )    % jesli x mniejsze od wartosci najwiekszej, to ... 
     n=n+1, x=2*x;        % zwieksz licznik, pomnoz x przez dwa = zwieksz wykladnik o 1
     num2bitstr( x );     % pokaz bity
     %pause                % analizuj je
  end                     % eksponenta=[   1]-1023=-1022  <--   1 zwiazane z realmin
  n=n+2                   % eksponenta=[2047]-1023=+1024  <--2047 zwiazane z realmax   
  nbits = log2(n),        %                         2046
                          %                        +   2
end                       %                         2048
