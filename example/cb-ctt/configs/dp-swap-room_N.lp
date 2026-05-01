#const n = 0.

_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_project((assigned,3), assigned(C,D,P)) :- assigned(C,D,P).

_destroy((day_period,n), assigned(C,R,D,P), (D,P)) :- assigned(C,R,D,P).
_destroy((day_period,n), n(n)).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), assigned(C,D,P)) :- assigned(C,D,P).
_prioritize((1,true), 1, true).

_config("DP-Swap-Room", ((assigned,4);(assigned,3)), (day_period,n), (1,true)).

_strategy(roulette, "DP-Swap-Room").
