clc; clear; close all;

seed = 42;
N = 1e5;

methods = [
    "Numerical Recipes",
    "Borland C/C++",
    "Borland Delphi, Vurtual Pascal",
    "GNU Compiler Collection",
    "ANSI C",
    "POSIX C",
    "Microsoft Visual C/C++",
];


% for k=1:length(methods)
%     method = methods(k);
%     y = rand_multadd(N, seed, method);
%     figure;
%     hist(y);
%     title(method + " N = " + num2str(N));
% end




function counter = find_period(a, m, p, seed)
    first_val = mod(seed*a+m,p);
    counter = 0;
    
    current_val = first_val;
    for i = 1:p+1
        current_val = mod(current_val * a + m, p);
        counter = counter + 1;
        if current_val == first_val
            return;
        end
    end
end

trivial_period = find_period(2, 0, 4, 2)

tic
posixC_period = find_period(1103515245, 12345, 1024, 42)
period_calculation_time = toc
