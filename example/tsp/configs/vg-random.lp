_project((cycle,2), cycle(X,Y)) :- cycle(X,Y).

_destroy((random,auto), cycle(X,Y), (X,Y)) :- cycle(X,Y).
_destroy((random,auto), auto).

_prioritize((1,true), cycle(X,Y)) :- cycle(X,Y).
_prioritize((1,true), 1, true).

_config("VG-Random", (cycle,2), (random,auto), (1,true)).

_strategy(roulette, "VG-Random").
