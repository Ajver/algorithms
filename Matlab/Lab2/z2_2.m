clc; clear all; close all;


a=fi( 1.625,0,8,7), a.bin,
b=fi( 0.375,0,8,7), b.bin,
c=fi( 0.375,1,8,7), c.bin,
d=fi(-0.375,1,8,7), d.bin,

%% pi
pi2 = fi(pi, 0, 8, 7), pi2.bin   %11111111
pi2 = fi(pi, 0, 16, 7), pi2.bin  %0000000110010010

pi2 = fi(pi, 1, 8, 7), pi2.bin   %01111111
pi2 = fi(pi, 1, 16, 7), pi2.bin  %0000000110010010
% Zwiekszanie precyzji float (np. z 7 -> 13) zwieksza precyzje liczby pi

pi3 = double(pi2)
err = pi3 - pi