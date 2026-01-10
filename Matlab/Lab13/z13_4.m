% rand_transform2.m
% Przekształcenie Boxa-Millera

clc; clear; close all;

m = 2.4
s = 1.7

function x = to_custom_norm(z, m, s)
    x = z*s + m;
end

disp('Równomierny R[0,1] --> Normalny (m,s)')
N = 10000; 
r1 = rand(1,N);
r2 = rand(1,N);
figure;
subplot(111); plot(r1,r2,'b*'); xlabel('r1'); ylabel('r2'); grid;  
figure;
subplot(211); hist(r1,20); title('hist( r1 )'); axis([0,1,0,1000]); grid;
subplot(212); hist(r2,20); title('hist( r2 )'); axis([0,1,0,1000]); grid; 


n1 = sqrt(-2*log(r1)) .* cos(2*pi*r2);
n2 = sqrt(-2*log(r1)) .* sin(2*pi*r2);

figure;
subplot(111); plot(n1,n2,'b*'); xlabel('n1'); ylabel('n2'); grid; axis equal;
figure;
subplot(211); hist(n1,20); title('hist( n1 )'); axis([-5,5,0,2000]); grid;
subplot(212); hist(n2,20); title('hist( n2 )'); axis([-5,5,0,2000]); grid; 

n1 = to_custom_norm(n1, m, s);
n2 = to_custom_norm(n2, m, s);

figure;
subplot(211); hist(n1,20); axis([-8,8,0,2000]); grid;
xline(mean(n1), color="red", LineWidth=3);
legend("std="+num2str(std(n1)), "m=" + num2str(mean(n2)));
title("n1, custom Normal \mu = " + num2str(m) + ", \sigma = " + num2str(s))
subplot(212); hist(n2,20); title('hist( n2 )'); axis([-8,8,0,2000]); grid; 
xline(mean(n2), color="red", LineWidth=3);
legend("std="+num2str(std(n2)), "m=" + num2str(mean(n2)));

