% svd_image.m
clear all; close all;

[X,map] = imread('lena512.bmp');         % wczytaj obraz
wymiary = size(X), 

X = double(X);                           % pokaz go
figure; image(X); title('Oryginal');
colormap(map); axis image off; pause

[U,S,V] = svd(X);                        % zrob dekompozycje SVD
figure; image( U*S*V' ); title('SVD');           % odtworz obraz ze wszystkich skladowych
colormap(map); axis image off; pause
figure; stem(diag(S)); title('Wartosci osobliwe'); pause

mv=[1, 2, 3, 4, 5, 10, 15, 20, 25, 50];  % okresl liczbe skladowych
for i = 1:length(mv)                     % PETLA - START
    mv(i)                                % wybrana liczba skladowych
    mask = zeros( size(S) );             % maska zerujaca wartosci osobliwe (w.o.)
    mask( 1:mv(i), 1:mv(i) ) = 1;        % wstaw "1" pozostawiajace najwieksze w.o. 
    figure; image( U*(S.*mask)*V' );     % synteza i pokaznie obrazu zrekonstruowanego
    colormap(map); axis image off;       % bez osi
    pause                                % a widzisz?
end                                      % PETLA - STOP
