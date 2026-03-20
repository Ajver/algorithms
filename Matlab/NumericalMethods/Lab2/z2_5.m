clc; clear all; close all;

disp('FLOAT: Dokladnosc');
disp('1 + 2ˆ(-24)'); num2bitstr( single( 1 + 2^(-24) ));
disp('1 + 2ˆ(-23)'); num2bitstr( single( 1 + 2^(-23) ));
disp('1 + 2ˆ(-22)'); num2bitstr( single( 1 + 2^(-22) ));
disp('1 + 2ˆ(-21)'); num2bitstr( single( 1 + 2^(-21) ));
disp('1 + 2ˆ(-21) + 2ˆ(-23)');
num2bitstr( single( 1 + 2^(-21) + 2^(-23) ));
disp('1 + 2ˆ(-53) + 2ˆ(-53) ');
hex2bitstr( num2hex( 1 + 2^(-53) + 2^(-53) ));
disp(' 2ˆ(-53) + 2ˆ(-53) + 1');
hex2bitstr( num2hex( 2^(-53) + 2^(-53) + 1 ));
disp(' ');