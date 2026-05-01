#const n = 0.

_project((hint,3), hint(R,C,N)) :- hint(R,C,N).

_destroy((random,n), hint(R,C,N), (R,C,N)) :- hint(R,C,N).
_destroy((random,n), p(n)).

_prioritize((1,true), hint(R,C,N)) :- hint(R,C,N).
_prioritize((1,true), 1, true).

_config("Random", (hint,3), (random,n), (1,true)).

_strategy(roulette, "Random").
