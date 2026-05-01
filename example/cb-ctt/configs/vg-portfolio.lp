_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_project((assigned,3), assigned(C,D,P)) :- assigned(C,D,P).

_destroy((random,auto), assigned(C,R,D,P), (C,R,D,P)) :- assigned(C,R,D,P).
_destroy((random,auto), auto).

_destroy((day_period,(1;2)), assigned(C,R,D,P), (D,P)) :- assigned(C,R,D,P).
_destroy((day_period,N), n(N)) :- N=(1;2).

_destroy((day_room,1), assigned(C,R,D,P), (D,R)) :- assigned(C,R,D,P).
_destroy((day_room,1), n(1)).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), assigned(C,D,P)) :- assigned(C,D,P).
_prioritize((1,true), 1, true).

_config("VG-Random", (assigned,4), (random,auto), (1,true)).

_config("Day-Period", (assigned,4), (day_period,1), (1,true)).

_config("Day-Room", (assigned,4), (day_room,1), (1,true)).

_config("VG-Swap-Room", (assigned,(4;3)), (random,auto), (1,true)).

_config("DP-Swap-Room 2", (assigned,(4;3)), (day_period,2), (1,true)).

_strategy(roulette,C) :- _config(C,_,_,_).
