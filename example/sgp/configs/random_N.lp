#const n = 0.

_project((plays,3), plays(P,W,G)) :- plays(P,W,G).

_destroy((random,n), plays(P,W,G), W) :- plays(P,W,G).
_destroy((random,n), p(n)).

_prioritize((1,true), plays(P,W,G)) :- plays(P,W,G).
_prioritize((1,true), 1, true).

_config("Random", (plays,3), (random,n), (1,true)).

_strategy(roulette, "Random").
