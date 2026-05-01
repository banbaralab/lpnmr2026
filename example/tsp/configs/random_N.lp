#const n = 0.

_project((cycle,2), cycle(X,Y)) :- cycle(X,Y).

_destroy((random,n), cycle(X,Y), (X,Y)) :- cycle(X,Y).
_destroy((random,n), p(n)).

_prioritize((1,true), cycle(X,Y)) :- cycle(X,Y).
_prioritize((1,true), 1, true).

_config("Random", (cycle,2), (random,n), (1,true)).

_strategy(roulette, "Random").
