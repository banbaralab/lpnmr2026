_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).

_destroy((day_period,1), assigned(C,R,D,P), (D,P)) :- assigned(C,R,D,P).
_destroy((day_period,1), n(1)).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), 1, true).

_config("Day-Period", (assigned,4), (day_period,1), (1,true)).

_strategy(roulette, "Day-Period").
