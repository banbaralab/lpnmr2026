#const n = 0.
_project("assigned/4", assigned(C,R,D,P)) :- assigned(C,R,D,P).
_project("assigned/3", assigned(C,D,P)) :- assigned(C,D,P).
_destroy("random", assigned(C,R,D,P), (C,R,D,P)) :- assigned(C,R,D,P).
_destroy("random", auto).
_prioritize("heu-1,true", assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize("heu-1,true", assigned(C,D,P)) :- assigned(C,D,P).
_prioritize("heu-1,true", 1, true).
_config("swap-room-auto", ("assigned/4";"assigned/3"), "random", "heu-1,true").
_strategy(roulette, "swap-room-auto").
