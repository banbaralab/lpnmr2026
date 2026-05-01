_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).

_destroy((random,auto), assigned(C,R,D,P), (C,R,D,P)) :- assigned(C,R,D,P).
_destroy((random,auto), auto).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), 1, true).

_config("VG-Random", (assigned,4), (random,auto), (1,true)).

_strategy(roulette, "VG-Random").
