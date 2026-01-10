clc; clear; close all;

N = 11;

L = 2*(2^N);
buf = ones(1,N);
for n = 1 : L
if(N==2) y(n)=xor(buf(1), buf(2)); end % N=2 oct(7) 111
if(N==3) y(n)=xor(buf(2), buf(3)); end % N=3 oct(13) 1 011
if(N==4) y(n)=xor(buf(3), buf(4)); end % N=4 oct(23) 10 011
if(N==5) y(n)=xor(buf(3), buf(5)); end % N=5 oct(45) 100 101
if(N==9) y(n)=xor(buf(5), buf(9)); end % N=9 oct(1021) 1 000 010 001
if(N==12) y(n)=xor(buf(6), xor(buf(8), xor(buf(11), buf(12)))); end % N=12 oct(10123) 1 000 001 010 011

if(N==6) y(n)=xor(buf(5), buf(6)); end % N=6 oct(103) 1 000 011
if(N==7) y(n)=xor(buf(4), buf(7)); end % N=7 oct(211) 10 001 001
if(N==8) y(n)=xor(buf(4), xor(buf(5), xor(buf(6), buf(8)))); end % N=6 oct(435) 100 011 101
if(N==10) y(n)=xor(buf(7), buf(10)); end % N=10 oct(2011) 10 000 001 001
if(N==11) y(n)=xor(buf(9), buf(11)); end % N=11 oct(4005) 100 000 000 101

buf = [ y(n) buf(1:N-1) ];
end
figure;
subplot(211); stem(y,'bo'); title('y(n)')
subplot(212); stem(-L+1:L-1,xcorr(y-mean(y))); grid; title('Ryy(k)'); axis tight;

xc = xcorr(y-mean(y));
[m, period] = max(xc(L+1:length(xc)));
period

