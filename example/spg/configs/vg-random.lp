_project((hint,3), hint(R,C,N)) :- hint(R,C,N).

_destroy((random,auto), hint(R,C,N), (R,C,N)) :- hint(R,C,N).
_destroy((random,auto), auto).

_prioritize((1,true), hint(R,C,N)) :- hint(R,C,N).
_prioritize((1,true), 1, true).

_config("VG-Random", (hint,3), (random,auto), (1,true)).

_strategy(roulette, "VG-Random").
