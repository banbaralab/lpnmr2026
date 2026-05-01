% solve instance g-p-w of the social-golfer problem
% schedule a group of n=g*p golfers into g groups of p players for w weeks such
% that no two golfers play in the same group more than once.

#const g=8.
#const p=4.
#const w=10.

#show plays/3.

player(0..g*p-1).
group(0..g-1).
% week(0..w-1).

% each player plays in each week in exactly one group
{ plays(P,W,G) : group(G) } = 1 :- player(P), week(W).

% the size of each group is 'p'
{ plays(P,W,G) : player(P) } = p :- week(W), group(G).

% players should not meet more than once
% minimize times a golfer meets more than once
meets(P1,P2,W)  :- plays(P1,W,G), plays(P2,W,G), P1 < P2.
:~ #count { W : meets(P1,P2,W) } > 1, player(P1), player(P2), P1 < P2. [1,P1]
%:~ meets(P1,P2,W1), meets(P1,P2,W2), W1 < W2. [1,P1]

% minimize conflict positions in the schedule
%conflict(P,W,G) :- plays(P,W,G), plays(P1,W,G), P1 != P,
%                   plays(P,W1,G1), W1 < W, plays(P1,W1,G1).
%:~ conflict(P,W,G). [1,P,W,G]

% maximize sozialisation = sum of golfers any golfer meets
% meets(P1,P2,W)  :- plays(P1,W,G), plays(P2,W,G), P1 != P2.
% meets(P,N) :- player(P), N = #count { P1: meets(P,P1,W)  }. 
% :~ meets(P,N). [-N,P]

%conflict(P1,P2) :- player(P1), player(P2), P1 < P2,
%                   #count { W : meets(P1,P2,W) } > 1.

% conflict_pos(P,W,G) :- plays(P,W,G), conflict(P,P2), plays(P2,W,G).
% conflict_pos(P,W,G) :- plays(P,W,G), conflict(P2,P), plays(P2,W,G).

%:~ conflict(P1,P2). [1,P1,P2]

