_project((plays,3), plays(P,W,G)) :- plays(P,W,G).

_destroy((random,auto), plays(P,W,G), W) :- plays(P,W,G).
_destroy((random,auto), auto).

_prioritize((1,true), plays(P,W,G)) :- plays(P,W,G).
_prioritize((1,true), 1, true).

_config("VG-Random", (plays,3), (random,auto), (1,true)).

_strategy(roulette, "VG-Random").
