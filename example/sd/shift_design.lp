%%%%%%%%%%%%%%%%%%%%%
% DOMAIN PREDICATES %
%%%%%%%%%%%%%%%%%%%%%

#const extra = 0. % change value to activate redundant constraints on shift starts
#const timeslots = days*timeslots_per_day.

day(0..days-1).
time(0..timeslots_per_day-1).
slot(0..timeslots-1).

next_time(T,(T+1)\timeslots_per_day) :- time(T).
next_slot(S,(S+1)\timeslots)         :- slot(S).

positive(S)   :- slot(S), required(S,R), 0 < R.
positive(S,R) :- positive(S), R = #max{ T : required(S,T) }.

excess_limit(S,M+R) :- limit(excess,M), positive(S,R).
excess_limit(S,M)   :- limit(excess,M), slot(S), not positive(S).
excess_limit        :- excess_limit(S,M).

shift_length(N,L-BL..L+AL)                    :- shift_length(N,L,AL,BL).
shift_start((T+AT)\timeslots_per_day,L,BT+AT) :- shift_start(N,T,AT,BT),
                                                 shift_length(N,L), 0 < L.
shift_start(T1,L,C-1)                         :- shift_start(T2,L,C),
                                                 next_time(T1,T2), 0 < C.
shift_start(T,L)                              :- shift_start(T,L,C).

shift_slot(timeslots_per_day*D+T,L) :- shift_start(T,L), day(D).

forward(S0,L,S0,L)   :- shift_slot(S0,L).
forward(S0,L,S2,C-1) :- forward(S0,L,S1,C), next_slot(S1,S2), 1 < C.
forward(S1,C)        :- forward(S0,L,S1,C).

revisit(S,C,(C+timeslots-1)/timeslots) :- forward(S,C).

restrict(S2,1,M) :- forward(S2,1), excess_limit(S2,M).
restrict(S1,C,P) :- revisit(S1,C,F), excess_limit(S1,M), next_slot(S1,S2), restrict(S2,C-1,N),
                    G = M/F, P = (G+N-|G-N|)/2.

demand(S,C,(R+F-1)/F) :- revisit(S,C,F), positive(S,R).

usage(S1,L,S2,C,M) :- forward(S1,L,S2,C), demand(S2,C,M), not forward(S1,L,S2,C+timeslots).
usage(S1,L,M)      :- usage(S1,L,S2,C,M).
usage(S1,L)        :- usage(S1,L,M).

max_usage(S,L,N) :- usage(S,L), N = #max{ M : usage(S,L,M) }.
max_start(S,L,M) :- usage(S,L), M = #min{ N : max_usage(S,L,N); P : restrict(S,L,P) }.

can_start(S,L,1..M) :- max_start(S,L,M).
can_start(S,L)      :- can_start(S,L,1).
can_start(S)        :- can_start(S,L).
max_start(S,M)      :- can_start(S), M = #max{ L : can_start(S,L) }.

can_run(S2,C) :- can_start(S1,L), forward(S1,L,S2,C).
can_run(S)    :- can_run(S,C).
max_run(S,M)  :- can_run(S), M = #max{ C : can_run(S,C) }.
min_run(S,N)  :- can_run(S), N = #min{ C : can_run(S,C) }.

dominate(S2,C) :- next_slot(S1,S2), can_run(S2,C), max_run(S1,M), C < M.
dominate(S)    :- dominate(S,C).

initiate(S2,L)   :- next_slot(S1,S2), can_start(S2,L), not can_run(S1,L+1).
initiate(S1,C+1) :- next_slot(S1,S2), initiate(S2,C), dominate(S2,C).

ordering(S,C) :- initiate(S,C), not dominate(S,C).
ordering(S)   :- ordering(S,C).
continue(S,M) :- ordering(S), M = #min{ C : ordering(S,C) }.


%order(S1,C1,C2)     :- ordering(S1,(C1;C2)), C1 < C2, C <= C1 : ordering(S1,C), C < C2.
%order(S1,C1,C2)     :- ordering(S1,(C1,C2)), C1 < C2, C <= C1 : ordering(S1,C), C < C2.
% order(S1,C1,C2)     :- ordering(S1,C1), ordering(S1,C2), ordering(S1,C), C1 < C2, C <= C1, C < C2.

% order(S1,C1,C2)     :- ordering(S1,C1), ordering(S1,C2), ordering(S1,C), C1 < C2, C <= C1, C < C2.
order(S1,C1,C2)     :- ordering(S1,C1), ordering(S1,C2), C1 < C2, C <= C1: ordering(S1,C), C < C2.
order(S1,C1,C2)     :- dominate(S1), continue(S1,C2), C1 = #max{ C : dominate(S1,C) }.
order(S2,C1-1,C2-1) :- order(S1,C1,C2), next_slot(S1,S2), 1 < C1.

close(S2,C)      :- next_slot(S1,S2), can_run(S1,C+1), max_start(S2,L), 0 < C, C < L.
close(S,C1,C2)   :- order(S,C1,C2), close(S,C2).
close(S,C1,C2)   :- order(S,C1,C2), min_run(S,C2).
close(S,C1,C2)   :- order(S,C1,C2), close(S,C2,C3).
close(S,C1,C2,I) :- order(S,C1,C2), can_start(S,C2,I), not close(S,C1,C2).
close(S,C1,C2,I) :- order(S,C1,C2), close(S,C2,C3,I), not close(S,C1,C2).

track(S1,C+1) :- next_slot(S1,S2), close(S2,C).
track(S1,C)   :- next_slot(S1,S2), can_run(S1,C), can_start(S2,C-1).
track(S1,C)   :- next_slot(S1,S2), can_run(S1,C), track(S2,C-1).

outer(S,C,P)    :- close(S,C), restrict(S,C,P).
outer(S,C,#sup) :- close(S,C), not excess_limit.

leave(S,L)    :- max_start(S,L,M), demand(S,L,N), M <= N, extra != 0.
leave(S,L)    :- usage(S,L,S1,C,M), restrict(S1,C,P), P <= M, extra != 0.
check(S,L)    :- can_start(S,L), extra != 0, not leave(S,L).
leave(S,L,C1) :- check(S,L), usage(S,L,S1,C1,M), usage(S,L,S2,C2,N), C1 < C2, M <= N.

admit(S,L,I,S1,C,M+1-I) :- check(S,L), can_start(S,L,I), usage(S,L,S1,C,M), I <= M,
                           not leave(S,L,C).
admit(I,S1,C,N)         :- admit(S,L,I,S1,C,N).
trans(S,L,I)            :- admit(S,L,I,S1,C,N), admit(S2,K,I,S1,C,N), L < K.
final(S,L,I)            :- check(S,L), can_start(S,L,I), not trans(S,L,I).

%%%%%%%%%%%%%%%%%
% GENERATE+TEST %
%%%%%%%%%%%%%%%%%

{ cover(S,L,I) } :- can_start(S,L,I).
cover(S,C1,I)    :- cover(S,C2,I), close(S,C1,C2).
cover(S,C1,I)    :- cover(S,C2,I), close(S,C1,C2,I).
cover(S2,C-1,I)  :- cover(S1,C,I), next_slot(S1,S2), min_run(S2,N), N < C.
cover(S2,C1,K)   :- cover(S2,C2,I), next_slot(S1,S2), order(S2,C1,C2), outer(S2,C1,P),
                    run(S1,C1+1,J), K = I+J, K <= P.
:- cover(S2,C2,P+1-J), next_slot(S1,S2), order(S2,C1,C2), close(S2,C1), restrict(S2,C1,P),
   run(S1,C1+1,J).
:- cover(S,C,I), 1 < I, not cover(S,C,I-1).
:- positive(S,R), min_run(S,N), limit(shortage,M), M < R, not cover(S,N,R-M).

run(S,L,I,1)   :- can_start(S,L,I), cover(S,L,I), not cover(S,C,I) : order(S,L,C).
run(S,L,I,N+1) :- run(S,L,I+1,N), 0 < I, not cover(S,C,I) : order(S,L,C).

run(S,L,N)  :- run(S,L,I,N).
run(S2,C,N) :- run(S1,C+1,N), next_slot(S1,S2), track(S2,C).
:- run(S,C,N), 1 < N, not run(S,C,N-1).

start(S2,L,N) :- can_start(S2,L,N), next_slot(S1,S2), run(S2,L,N), not run(S1,L+1,N).

clear(S2,C1,I)  :- admit(I,S2,C1,N), not cover(S2,C2,N) : order(S2,C1,C2).
clear(S1,C+1,I) :- next_slot(S1,S2), clear(S2,C,I), not final(S2,C,I).
:- check(S,L), start(S,L,I), not clear(S,L,I).

%%%%%%%%%%%%
% OPTIMIZE %
%%%%%%%%%%%%

:~ cover(S,N,I), min_run(S,N), not positive(S), optimize(excess,W,P). [ W@P,excess,S,I ]
:~ cover(S,N,I), min_run(S,N), positive(S,R), R < I, optimize(excess,W,P). [ W@P,excess,S,I ]

:~ positive(S,R), min_run(S,N), K = #min{ R; M : limit(shortage,M) },
   I = R+1-K..R, not cover(S,N,I), optimize(shortage,W,P). [ W@P,shortage,S,I ]

:~ start(S,L,N), optimize(selected_shift,W,P). [ W@P,selected_shift,S\timeslots_per_day,L ]

% Optimization criteria: Property, Weight, Level
optimize(selected_shift,1,1).
optimize(shortage,1,3).
optimize(excess,1,2).

%%%%%%%%%%%
% DISPLAY %
%%%%%%%%%%%

#show start/3.