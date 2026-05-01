#const n = 0.

_project((unit2zone,2), unit2zone(U,Z)) :- unit2zone(U,Z).
_project((unit2sensor,2), unit2sensor(U,S)) :- unit2sensor(U,S).

_destroy((random,n), unit2zone(U,Z), (U,Z)) :- unit2zone(U,Z).
_destroy((random,n), unit2sensor(U,S), (U,S)) :- unit2sensor(U,S).
_destroy((random,n), p(n)).

_prioritize((1,true), unit2zone(U,Z)) :- unit2zone(U,Z).
_prioritize((1,true), unit2sensor(U,S)) :- unit2sensor(U,S).
_prioritize((1,true), 1, true).

_config("Random", ((unit2zone,2);(unit2sensor,2)), (random,n), (1,true)).

_strategy(roulette, "Random").
