a=fi( 11.25,0,8,4), a.bin,
b=fi( 4.75,0,8,4), b.bin,
c=fi( 4.75,1,8,4), c.bin,
d=fi(-4.75,1,8,4), d.bin,

%% pi
pi2 = fi(pi, 0, 8, 6), pi2.bin   %01111111
pi2 = fi(pi, 0, 16, 12), pi2.bin  %0011001001000100

pi2 = fi(pi, 1, 8, 6), pi2.bin   %01111111
pi2 = fi(pi, 1, 16, 12), pi2.bin  %0011001001000100
% Zwiekszanie precyzji float (np. z 7 -> 13) zwieksza precyzje liczby pi

pi3 = double(pi2)
err = pi3 - pi