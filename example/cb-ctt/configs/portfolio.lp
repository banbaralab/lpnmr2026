_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_project((assigned,3), assigned(C,D,P)) :- assigned(C,D,P).

_destroy((random,(6;10)), assigned(C,R,D,P), (C,R,D,P)) :- assigned(C,R,D,P).
_destroy((random,N), p(N)) :- N=(6;10).

_destroy((day_period,(1;2)), assigned(C,R,D,P), (D,P)) :- assigned(C,R,D,P).
_destroy((day_period,N), n(N)) :- N=(1;2).

_destroy((day_room,1), assigned(C,R,D,P), (D,R)) :- assigned(C,R,D,P).
_destroy((day_room,1), n(1)).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), assigned(C,D,P)) :- assigned(C,D,P).
_prioritize((1,true), 1, true).

_config("Random 6%", (assigned,4), (random,6), (1,true)).

_config("Day-Period", (assigned,4), (day_period,1), (1,true)).

_config("Day-Room", (assigned,4), (day_room,1), (1,true)).

_config("Swap-Room 10%", (assigned,(4;3)), (random,10), (1,true)).

_config("DP-Swap-Room 2", (assigned,(4;3)), (day_period,2), (1,true)).

_strategy(roulette,C) :- _config(C,_,_,_).
