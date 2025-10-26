clc; clear all; close all;

x = [1, 2, 3, 4];
y = [-3, -2, 4, 6];
xi = [0:0.01:5];

[yi_org,a_org] = funTZ_lagrange(x,y,xi);
[yi_moj, a_moj] = moja_fun_lagrange_z5_6(x, y, xi);
yii_org = polyval(a_org, xi);

figure; plot(x,y,'ro',xi,yi_org,'b-',xi,yii_org,'k-'); title('y=f(x)');   % rysunek

blad_a = a_org - a_moj
blad_yi = sum((yi_org - yi_moj).^2)  % SSE
