#const n = 0.

_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).

_destroy((random,n), assigned(C,R,D,P), (C,R,D,P)) :- assigned(C,R,D,P).
_destroy((random,n), p(n)).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), 1, true).

_config("Random", (assigned,4), (random,n), (1,true)).

_strategy(roulette, "Random").
