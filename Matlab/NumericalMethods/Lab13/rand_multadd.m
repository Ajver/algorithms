function s=rand_multadd( N, seed, method )

switch method
    case "Numerical Recipes"
        a = 1664525; m = 1013904223; p = 2^32;
    case "GNU Compiler Collection"
        a = 69069; m = 5; p = 2^32;
    case "Borland C/C++"
        a = 22695477; m = 1; p = 2^32;
    case "Borland Delphi, Vurtual Pascal"
        a = 134775813; m = 1; p = 2^32;
    case "ANSI C"
        a = 1103515245; m = 12345; p = 2^32;
    case "POSIX C"
        a = 1103515245; m = 12345; p = 2^31;
    case "Microsoft Visual C/C++"
        a = 214013; m = 2531011; p = 2^32;

    otherwise
        e = "unknown method: " + method
        error("unknown method: " + method)
end

s = zeros(N,1);
for i=1:N
    seed = mod(seed*a+m,p);
    s(i) = seed;
end

% TEST  
%   figure; w=s-mean(s); plot(-9999:9999,xcorr(w,w),'o-');
%   z = 1:4096;  [ s(z), s(z+1*1024)], pause
s = s/p;