

Ze = 50
Zs1 = 50
Zs2 = 50
Zd = 50
Z0 = 50

E = 12

A = [ 1/Ze + 1/Zs1, -1/Zs1,                 0; ...
      -1/Zs1,       1/Zs1 + 1/Zs2 + 1/Zd, -1/Zs2,
      0,            -1/Zs2,               1/Zs2 + 1/Z0   ]

B = [ E/Ze; 0; 0 ]

% Ax = B
x = inv(A) * B


