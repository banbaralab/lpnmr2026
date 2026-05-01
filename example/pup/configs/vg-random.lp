_project((unit2zone,2), unit2zone(U,Z)) :- unit2zone(U,Z).
_project((unit2sensor,2), unit2sensor(U,S)) :- unit2sensor(U,S).

_destroy((random,auto), unit2zone(U,Z), (U,Z)) :- unit2zone(U,Z).
_destroy((random,auto), unit2sensor(U,S), (U,S)) :- unit2sensor(U,S).
_destroy((random,auto), auto).

_prioritize((1,true), unit2zone(U,Z)) :- unit2zone(U,Z).
_prioritize((1,true), unit2sensor(U,S)) :- unit2sensor(U,S).
_prioritize((1,true), 1, true).

_config("VG-Random", ((unit2zone,2);(unit2sensor,2)), (random,auto), (1,true)).

_strategy(roulette, "VG-Random").
