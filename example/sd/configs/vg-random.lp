_project((start,3), start(S,L,N)) :- start(S,L,N).

_destroy((random,auto), start(S,L,N), (S,L,N)) :- start(S,L,N).
_destroy((random,auto), auto).

_prioritize((1,sign), start(S,L,N)) :- start(S,L,N).
_prioritize((1,sign), 1, sign).

_config("VG-Random", (start,3), (random,auto), (1,sign)).

_strategy(roulette, "VG-Random").
