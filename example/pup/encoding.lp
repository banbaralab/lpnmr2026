zone(Z) :- zone2sensor(Z, _).
sensor(S) :- zone2sensor(_, S).

1 { unit2zone(U, Z) : unit(U) } 1 :- zone(Z).
1 { unit2sensor(U, S) : unit(U) } 1 :- sensor(S).

:- unit(U), unitCap(C), C + 1 { unit2zone(U, Z) : zone(Z) }.
:- unit(U), unitCap(C), C + 1 { unit2sensor(U, S) : sensor(S) }.

partnerunits(U, P) :- unit2zone(U, Z), zone2sensor(Z, S), unit2sensor(P, S), U != P.
partnerunits(U, P) :- partnerunits(P, U), unit(U), unit(P).

:- unit(U), interUnitCap(C), C + 1 { partnerunits(U, P) : unit(P) }.

%%%%%%%%%%%%%%%%%% optimization %%%%%%%%%%%%%%%%%%
unitUsed(U) :- unit2zone(U, Z).
unitUsed(U) :- unit2sensor(U, S).
L { unitUsed(X) : unit(X) } U :- lower(L), upper(U).
#minimize{ 1, X : unitUsed(X) }.