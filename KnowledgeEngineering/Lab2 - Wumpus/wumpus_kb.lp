% Wumpus world knowledge base (agent's view).
%
% Every stable model of this program is one way the hidden part of the cave
% could look that is consistent with everything the agent has perceived.
% The Python side asks clingo for
%   * cautious consequences (true in ALL models)  -> what the agent KNOWS,
%   * brave consequences    (true in SOME model)  -> what is POSSIBLE.
%
% Facts supplied by the agent (see inference.py):
%   size(W, H).            world dimensions (known to the agent)
%   wumpus_count(K).       number of wumpuses in the cave
%   visited(X, Y).         cells the agent has stood on (and survived)
%   breeze(X, Y).    / no_breeze(X, Y).   percepts at visited cells
%   stench(X, Y).    / no_stench(X, Y).
%   shot(N, X, Y, D).      N-th arrow shot from (X, Y) in direction D (n/e/s/w)
%   scream(N).       / no_scream(N).      whether a scream followed shot N

#defined visited/2.
#defined breeze/2.    #defined no_breeze/2.
#defined stench/2.    #defined no_stench/2.
#defined shot/4.
#defined scream/1.    #defined no_scream/1.

% --- geometry ---------------------------------------------------------------
delta(n, 0, 1). delta(e, 1, 0). delta(s, 0, -1). delta(w, -1, 0).
cell(1..W, 1..H) :- size(W, H).
start(1, 1).
adj(X, Y, X+DX, Y+DY) :- cell(X, Y), delta(_, DX, DY), cell(X+DX, Y+DY).

% Unvisited cells next to a visited one. Pits elsewhere cannot influence any
% percept, so they are left out of the guess (this keeps models small); the
% agent treats pits in such cells as unknown.
frontier(X, Y) :- adj(X, Y, A, B), visited(A, B), not visited(X, Y).

% --- guess the hidden world -------------------------------------------------
{ pit(X, Y) } :- frontier(X, Y).
K { wumpus(X, Y) : cell(X, Y), not start(X, Y) } K :- wumpus_count(K).

% --- percepts must agree with the guess -------------------------------------
near_pit(X, Y) :- adj(X, Y, A, B), pit(A, B).
:- breeze(X, Y), not near_pit(X, Y).
:- no_breeze(X, Y), near_pit(X, Y).

% Dead wumpuses still stink.
near_wumpus(X, Y) :- adj(X, Y, A, B), wumpus(A, B).
:- stench(X, Y), not near_wumpus(X, Y).
:- no_stench(X, Y), near_wumpus(X, Y).

% --- arrows -----------------------------------------------------------------
% Cells on the path of arrow N, with distance I from the shooter.
on_ray(N, X+DX*I, Y+DY*I, I) :-
    shot(N, X, Y, D), delta(D, DX, DY), size(W, H), I = 1..W+H,
    cell(X+DX*I, Y+DY*I).

% A wumpus is alive when arrow N flies unless an earlier arrow killed it.
killed_before(N, X, Y) :- shot(N, _, _, _), hit(M, X, Y), M < N.
alive_before(N, X, Y)  :- shot(N, _, _, _), wumpus(X, Y), not killed_before(N, X, Y).

% The arrow stops at the first living wumpus on its path.
shadowed(N, I) :- on_ray(N, X, Y, J), alive_before(N, X, Y), on_ray(N, _, _, I), J < I.
hit(N, X, Y)   :- on_ray(N, X, Y, I), alive_before(N, X, Y), not shadowed(N, I).

screams(N) :- hit(N, _, _).
:- scream(N), not screams(N).
:- no_scream(N), screams(N).

dead(X, Y)  :- hit(_, X, Y).
alive(X, Y) :- wumpus(X, Y), not dead(X, Y).

% The agent survived every visited cell, so no live wumpus can be there.
% (Pits are excluded from visited cells by construction of frontier/2.)
:- visited(X, Y), alive(X, Y).

% --- conclusions ------------------------------------------------------------
danger(X, Y) :- pit(X, Y).
danger(X, Y) :- alive(X, Y).
safe(X, Y)   :- frontier(X, Y), not danger(X, Y).

#show frontier/2.
#show pit/2.
#show wumpus/2.
#show alive/2.
#show dead/2.
#show safe/2.
