clc; clear all; close all;


% 10001101
a=fi( 141,0,8,0), a.bin,

% 01110011
b=fi( 115,0,8,0), b.bin,

% 01110011 = 01110010 + 1
c=fi( 115,1,8,0), c.bin,

% 10001101
d=fi(-115,1,8,0), d.bin,


%% Uro
% [0..0]00011101
uro = fi(29, 0, 8, 0), uro.bin
uro = fi(29, 1, 8, 0), uro.bin
uro = fi(29, 0, 16, 0), uro.bin
uro = fi(29, 1, 16, 0), uro.bin

% 1111111111100011
uro = fi(-29, 1, 16, 0), uro.bin