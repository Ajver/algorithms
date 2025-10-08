%% bin = float2bin(in)
% 
% by Dogac Basaran - Bogazici University
%  
%  in: Input positive floating number
% bin: Output binary stream (as string)
%
% Example usage:
% 
% float2bin(0.5)
%   ans = 0.1
% 
% float2bin(6.625)
%   ans = 110.101

function bin = float2bin(in)

decpart = dec2bin(floor(in));

in = in-floor(in);

n = -1;
floatpart = [];
while in~=0 || in>eps
    if in - 2^n < 0 
        floatpart = [floatpart '0'];
    else
        floatpart = [floatpart '1'];
        in = in - 2^n;
    end
    n = n - 1;
end
bin = [decpart '.' floatpart];

