_project((strategic,1), strategic(X)) :- strategic(X).

_destroy((random,auto), strategic(X), X) :- strategic(X).
_destroy((random,auto), auto).

_prioritize((1,true), strategic(X)) :- strategic(X).
_prioritize((1,true), 1, true).

_config("VG-Random", (strategic,1), (random,auto), (1,true)).

_strategy(roulette, "VG-Random").
