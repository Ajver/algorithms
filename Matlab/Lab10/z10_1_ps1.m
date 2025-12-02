% Znajdowanie minimum funkcji "bananowej" Rosenbrocka f(x1,x2) różnymi metodami
% f(x1,x2) = 100*(x2 - x1^2)^2 + (1-x1)^2
% Minimum: f(1,1) = 0

%  Sprawdź czy liczby wywołan funkcji i iteracji, podane w tabeli 10.1, 
% sa poprawne: NIE
% Analytic Gradient+Hessian 201 200

clear all; close all;

PAUSE = false;
results = {};
k = 1;

set(groot,'DefaultFigureColormap',hsv(64))

global a
global x0
global fun
a = 100;
fun = @(x)( a*(x(2) - x(1)^2)^2 + (1 - x(1))^2 );  % funkcja
x0 = [ -1.9, 2 ];                                   % punkt startowy

% fminsearch() - SIMPLEX
figure
options = optimset('OutputFcn',@bananaout,'Display','off');
[x,fval,eflag,output] = fminsearch(fun,x0,options);
title('Rosenbrock - via fminsearch() SIMPLEX'); 
if (PAUSE); pause; end
results{k,1} = 'Simplex';
results{k,2} = 'fminsearch()';
results{k,3} = output.funcCount;
results{k,4} = output.iterations;
Fcount = output.funcCount;
k = k + 1;
disp(['Number of function evaluations for fminsearch() SIMPLEX was ',num2str(Fcount)])
disp(['Number of solver iterations for fminsearch() SIMPLEX was ',num2str(output.iterations)])

% fminunc() - QUASI-NEWTON
figure
options = optimoptions('fminunc','Display','off',...
          'OutputFcn',@bananaout,'Algorithm','quasi-newton');
[x,fval,eflag,output] = fminunc( fun, x0, options );
title('Rosenbrock - fminunc() QUASI-NEWTON');  
if (PAUSE); pause; end
results{k,1} = 'Quasi-Newton';
results{k,2} = 'fminunc()';
results{k,3} = output.funcCount;
results{k,4} = output.iterations;
Fcount = output.funcCount;
k = k + 1;
disp(['Number of function evaluations for fminunc() QUASI-NEWTON was ',num2str(Fcount)])
disp(['Number of solver iterations for fminunc() QUASI-NEWTON was ',num2str(output.iterations)])

% fminunc() - STEEPEST-DESCENT
figure
options = optimoptions(options,'HessUpdate','steepdesc',...
          'MaxFunctionEvaluations',600);
[x,fval,eflag,output] = fminunc(fun,x0,options);
title('Rosenbrock - fminunc() STEEPEST-DESCENT');  
if (PAUSE); pause; end
results{k,1} = 'Steepest-Descent';
results{k,2} = 'fminunc()';
results{k,3} = output.funcCount;
results{k,4} = output.iterations;
Fcount = output.funcCount;
k = k + 1;
disp(['Number of function evaluations for fminunc() STEEPEST-DESCENT was ',num2str(Fcount)])
disp(['Number of solver iterations for fminunc() STEEPEST-DESCENT UPDATE was ',num2str(output.iterations)])

% fminunc() - ANALYTIC GRADIENT
figure
grad = @(x)[ -400*(x(2) - x(1)^2)*x(1) - 2*(1 - x(1)); ...   % first variable
             200*(x(2) - x(1)^2)];                           % second variable
fungrad = @(x)deal(fun(x),grad(x));
options = resetoptions(options,{'HessUpdate','MaxFunctionEvaluations'});
options = optimoptions(options,'SpecifyObjectiveGradient',true,...
'Algorithm','trust-region');
[x,fval,eflag,output] = fminunc(fungrad,x0,options);
title('Rosenbrock - fminunc() with ANALYTIC GRADIENT');  
if (PAUSE); pause; end
results{k,1} = 'Analytic Gradient';
results{k,2} = 'fminunc()';
results{k,3} = output.funcCount;
results{k,4} = output.iterations;
Fcount = output.funcCount;
k = k + 1;
disp(['Number of function evaluations for fminunc() ANALYTIC GRADIENT was ',num2str(Fcount)])
disp(['Number of solver iterations for fminunc() ANALYTIC GRADIENT was ',num2str(output.iterations)])

% fminunc() - ANALYTIC GRADIENT & HESSIAN
figure
hess = @(x)[ 1200*x(1)^2 - 400*x(2) + 2, -400*x(1);
             400*x(1),      200 ];
fungradhess = @(x)deal(fun(x),grad(x),hess(x));
options.HessianFcn = 'objective';
[x,fval,eflag,output] = fminunc(fungradhess,x0,options);
title('Rosenbrock - fminunc() ANALYTIC GRADIENT & HESSIAN');  
if (PAUSE); pause; end
results{k,1} = 'Analytic Gradient+Hessian';
results{k,2} = 'fminunc()';
results{k,3} = output.funcCount;
results{k,4} = output.iterations;
Fcount = output.funcCount;
k = k + 1;
disp(['Number of function evaluations for fminunc() ANALYTIC GRAD & HESSIAN was ',num2str(Fcount)])
disp(['Number of solver iterations for ANALYTIC HESSIAN was ',num2str(output.iterations)])

% lsqnonlin() - NON-LINEAR LEAST-SQUARES
figure
options = optimoptions('lsqnonlin','Display','off','OutputFcn',@bananaout);
vfun = @(x)[ 10*(x(2) - x(1)^2), 1 - x(1)];
[x,resnorm,residual,eflag,output] = lsqnonlin(vfun,x0,[],[],options);
title('Rosenbrock - lsqnonlin() NONLINEAR LEAST-SQUARES');  
if (PAUSE); pause; end
results{k,1} = 'Non-linear Least-Squares';
results{k,2} = 'lsqnonlin()';
results{k,3} = output.funcCount;
results{k,4} = output.iterations;
Fcount = output.funcCount;
k = k + 1;
disp(['Number of function evaluations for lsqnonlin() NONLINEAR LEAST-SQUARES was ',num2str(Fcount)])
disp(['Number of solver iterations for lsqnonlin() NONLINEAR LEAST-SQUARES was ',num2str(output.iterations)])

% lsqnonlin() - NON-LINEAR LEAST-SQUARES + JACOBIAN
figure
jac = @(x)[-20*x(1), 10; ...
                 -1, 0  ];
vfunjac = @(x)deal(vfun(x),jac(x));
options.SpecifyObjectiveGradient = true;
[x,resnorm,residual,eflag,output] = lsqnonlin(vfunjac,x0,[],[],options);
title('Rosenbrock - lsqnonlin() NONLIN-LS with JACOBIAN');  
if (PAUSE); pause; end
results{k,1} = 'Nonlinear LS + Analytic Jac.';
results{k,2} = 'lsqnonlin()';
results{k,3} = output.funcCount;
results{k,4} = output.iterations;
k = k + 1;
Fcount = output.funcCount;
disp(['Number of function evaluations for lsqnonlin() LS-NONLIN JACOBIAN was ',num2str(Fcount)])
disp(['Number of solver iterations for lsqnonlin() LS-NONLIN JACOBIAN was ',num2str(output.iterations)])

set(groot,'DefaultFigureColormap',parula(64))


resultsTable = cell2table(results, ...
    'VariableNames', {'NazwaMetody', 'NazwaFunkcji', 'LiczbaWywolanFunkcji', 'LiczbaIteracjiAlgorytmu'});
resultsTable = sortrows(resultsTable, 'LiczbaWywolanFunkcji', 'descend');

disp(' ');
disp('Tabela wyników (posortowana malejąco po Liczbie wywołań funkcji):');
disp(resultsTable);

% Przykład wyświetlenia tabeli w formacie podobnym do podanego (opcjonalnie)
disp(' ');
disp('Nazwa metody                      Nazwa funkcji       #wyw. funkcji  # iter. algorytmu');
disp('---------------------------------------------------------------------------------------');
for i = 1:size(resultsTable, 1)
    fprintf('%-33s %-20s %12d %18d\n', ...
        resultsTable.NazwaMetody{i}, ...
        resultsTable.NazwaFunkcji{i}, ...
        resultsTable.LiczbaWywolanFunkcji(i), ...
        resultsTable.LiczbaIteracjiAlgorytmu(i));
end
