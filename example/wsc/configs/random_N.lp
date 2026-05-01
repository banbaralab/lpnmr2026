#const n = 0.

_project((strategic,1), strategic(X)) :- strategic(X).

_destroy((random,n), strategic(X), X) :- strategic(X).
_destroy((random,n), p(n)).

_prioritize((1,true), strategic(X)) :- strategic(X).
_prioritize((1,true), 1, true).

_config("Random", (strategic,1), (random,n), (1,true)).

_strategy(roulette, "Random").
