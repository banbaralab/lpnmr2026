#const n = 0.

_project((start,3), start(S,L,N)) :- start(S,L,N).

_destroy((random,n), start(S,L,N), (S,L,N)) :- start(S,L,N).
_destroy((random,n), p(n)).

_prioritize((1,sign), start(S,L,N)) :- start(S,L,N).
_prioritize((1,sign), 1, sign).

_config("Random", (start,3), (random,n), (1,sign)).

_strategy(roulette, "Random").
