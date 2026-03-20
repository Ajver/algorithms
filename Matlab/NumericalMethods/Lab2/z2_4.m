clc; clear all; close all;

num2bitstr( single( (1+1/4)*2^(-124) )),
num2bitstr( single( -5.877472*10^(-38) ))

c = 299792458
s_c = num2bitstr(single(c))
d_c = num2bitstr(double (c))

vc = 0

% Odtworzenie c wg. algorytmu U2
c2 = binstr2num(d_c)

err = c2 - c