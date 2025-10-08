function decnum = binstr2num(binstr)
    size = length(binstr);
    
    if size == 32
        exponent_bits = 8;
        fraction_bits = 23;
        bias = 127;
        
        sign = (-1)^str2double(binstr(1));
        exponent = binstr(2:1+exponent_bits);
        significand = binstr(2+exponent_bits:end);
    elseif size == 64
        exponent_bits = 11;
        fraction_bits = 52;
        bias = 1023;
        
        sign = (-1)^str2double(binstr(1));
        exponent = binstr(2:1+exponent_bits);
        significand = binstr(2+exponent_bits:end);
    else
        error('Długość ciągu binarnego musi wynosić 32 lub 64 bity');
    end

    expVal = bin2dec(exponent) - bias;

    mantissa = 1;
    for k = 1:fraction_bits
        mantissa = mantissa + str2double(significand(k)) * 2^(-k);
    end

    decnum = sign * mantissa * 2^expVal;
end
