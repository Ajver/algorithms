
% PDE_plyta.m
% z wykładu o układach równań: Tp .... Tk, stała temp. góra i dół (duża płyta, ściana)
% A * x = b:
% A - macierz punktów (współczynników),
% x - wektor temperatur,
% b = warunki brzegowe
% równanie Laplace'a: Tleft + Tright + Tup + Tdown - 4*Tcenter = 0
clear all; close all;

Tp = 20;  Tk = -5;   % temperatura: dom (początek), otoczenie (koniec)
N = 9;               % liczba punktów, 3 x 3

%      Warunki brzegowe
%         p1  p2  p3
%         ----------
%  (Tp) | p1  p2  p3 | (Tk) 
%  (Tp) | p4  p5  p6 | (Tk)
%  (Tp) | p7  p8  p9 | (Tk)
%         ----------
%         p7  p8  p9

b = [ -Tp; ...  % punkt 1     
        0; ...  % punkt 2
      -Tk; ...  % punkt 3
      -Tp; ...  % punkt 4
        0; ...  % punkt 5
      -Tk; ...  % punkt 6
      -Tp; ...  % punkt 7
        0; ...  % punkt 8
      -Tk];     % punkt 9

% Równanie Laplace'a wewnątrz płyty - punkty powyżej i poniżej są uwzgl. w CENTRUM
% ŹLE - ponieważ punkty powyżej i poniżej powinny mieć takie same wartości jak sąsiedzi na płycie 
% A = [ -3  1  0  1  0  0  0  0  0; ... % punkt 1 - (-3) dwóch    sąsiadów, pkt powyżej
%        1 -4  1  0  1  0  0  0  0; ... % punkt 2 - (-4) trzech   sąsiadów, pkt powyżej
%        0  1 -3  0  0  1  0  0  0; ... % punkt 3 - (-3) dwóch    sąsiadów, pkt powyżej
%        1  0  0 -3  1  0  1  0  0; ... % punkt 4 - (-3) trzech   sąsiadów
%        0  1  0  1 -4  1  0  1  0; ... % punkt 5 - (-4) czterech sąsiadów
%        0  0  1  0  1 -3  0  0  1; ... % punkt 6 - (-3) trzech   sąsiadów
%        0  0  0  1  0  0 -3  1  0; ... % punkt 7 - (-3) dwóch    sąsiadów, pkt. poniżej
%        0  0  0  0  1  0  1 -4  1; ... % punkt 8 - (-4) trzech   sądiadów, pkt. ponizej
%        0  0  0  0  0  1  0  1 -3 ];   % punkt 9 - (-3) dwóch    sąsiasów, pkt. ponizej

A = [ -3  1  0  1  0  0  0  0  0; ... % pkt 1 - (-3)=sąsiad: 1=lewy bok,  2=dól, 3=prawo,     pkt powyżej taki sam
       1 -3  1  0  1  0  0  0  0; ... % pkt 2 - (-3)=sasiad: 1=lewo,      2=dół, 3=prawo,     pkt powyżej taki sam
       0  1 -3  0  0  1  0  0  0; ... % pkt 3 - (-3)=sąsiad: 1=lewo,      2=dół, 3=prawy bok, pkt powyżej taki sam
       1  0  0 -4  1  0  1  0  0; ... % pkt 4 - (-4) trzech   sąsiadów, lewy bok
       0  1  0  1 -4  1  0  1  0; ... % pkt 5 - (-4) czterech sąsiadów
       0  0  1  0  1 -4  0  0  1; ... % pkt 6 - (-4) trzech   sąsiadów, prawy bok
       0  0  0  1  0  0 -3  1  0; ... % pkt 7 - (-3)=sąsiad: 1=lewy bok, 2=góra, 3=prawo,  pkt. poniżej taki sam
       0  0  0  0  1  0  1 -3  1; ... % pkt 8 - (-3)=sąsiad: 1=lewo, 2=góra,  3=prawo,     pkt. poniżej taki sam
       0  0  0  0  0  1  0  1 -3 ];   % pkt 9 - (-3)=sąsiad: 1=lewo, 2=góra,  3=prawy bok, pkt. ponizej taki sam

% Punkty lewego i prawego boku są po lewej stronie równania: suma daje zero po prawej stronie.
% Po przeniesieniu punktów boków, o znanych wartościach, na prawą stronę,
% zostają one zanegowane: A*x = b.

disp('Rozkład temperatury 3x3:')
x = A \ b,
reshape( x, 3, 3)', pause
