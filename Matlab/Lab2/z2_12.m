clc; clear; clear all;

p=1:16

for k=p
    x=10^(k-1);

    disp("x= " + x )
    disp("f1 = " + sqrt(x)*(sqrt(x+1)-sqrt(x)));
    disp("f2 = " + sqrt(x)/(sqrt(x+1) + sqrt(x)));

    if(k==10)
        disp(sqrt(x+1) + " " + sqrt(x))
    end
    disp("---")
end