%% #const grid_sz=9.
%% #const subgrid_sz=3.

% guess hints
{ hint(R, C, N) : R = 1..grid_sz, C = 1..grid_sz, N = 1..grid_sz }.
#show hint/3.

% minimise number of hints
:~ hint(R, C, N). [1, R,C,N]

% guess completion 'a' and check if 'a' satisfies all constraints
a(R, C, N) :- hint(R, C, N).
{ a(R, C, N): N = 1..grid_sz } = 1 :- R = 1..grid_sz, C = 1..grid_sz.

:- a(R, C1, N), a(R, C2, N), C1 != C2.
:- a(R1, C, N), a(R2, C, N), R1 != R2.
:- a(R, C, N), a(R1, C1, N), R != R1, C != C1,
   (((R-1)/subgrid_sz)*subgrid_sz + (C-1)/subgrid_sz) =
   (((R1-1)/subgrid_sz)*subgrid_sz + (C1-1)/subgrid_sz).

% guess (with disjunction) counterexample to uniqueness of solution
b(R, C, N) : N = 1..grid_sz:- R = 1..grid_sz, C = 1..grid_sz.

% check (with a positive program) that 'b' is not a counterexample

saturate :- b(R, C, N1), hint(R, C, N2), N1 != N2.

saturate :- b(R, C1, N), b(R, C2, N), C1 != C2.
saturate :- b(R1, C, N), b(R2, C, N), R1 != R2.
saturate :- b(R, C, N), b(R1, C1, N), R != R1, C != C1,
  (((R-1)/subgrid_sz)*subgrid_sz + (C-1)/subgrid_sz) =
  (((R1-1)/subgrid_sz)*subgrid_sz + (C1-1)/subgrid_sz).

saturate :- equals(R,C) : (R,C) = (1..grid_sz, 1..grid_sz).
equals(R,C) :- a(R,C,N), b(R,C,N).

% if 'b' is not a counterexample, then saturate
b(R, C, N) :- saturate, R = 1..grid_sz, C = 1..grid_sz, N = 1..grid_sz.
:- not saturate.
