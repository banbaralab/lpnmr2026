# Supplementary Materials: Adaptive Large Neighborhood Prioritized Search for Optimization in Answer Set Programming

## The heulingo solver

Heulingo is an ASP-based implementation of Adaptive Large Neighborhood Prioritized Search (ALNPS).
ALNPS is a metaheuristic that iteratively seeks better solutions starting from an initial solution.
It alternates between performing  variability-guided destruction and
prioritized search on the current solution.

## Requirements

- python3 (version 3.10 or higher)

## Installation

| Supported back-end solvers    | Installation command         |
|-------------------------------|------------------------------|
| clingo only                   | `pip install .`              |
| clingo + clingo-dl            | `pip install ".[clingo-dl]"` |
| clingo + clingcon             | `pip install ".[clingcon]"`  |
| clingo + clingo-dl + clingcon | `pip install ".[all]"`       |

You can check a successful installation by running
```
heulingo -h
```

## Sample sessions

heulingo accepts a COP instance in ASP fact format, an ASP encoding for COP solving, and an ALNPS configuration.
heulingo can deal with any ASP encoding for optimization without any modification.
All we have to do is to add an ALNPS configuration.

The following are some sessions for solving Curriculum-based Course Timetabling (CB-CTT).
We use the [teaspoon](https://github.com/banbara/teaspoon) encoding for CB-CTT solving and
the best option of [s10479-018-2757-7](http://doi.org/10.1007/s10479-018-2757-7).

### heulingo with the ALNPS configuration VG-Random

```
heulingo --configuration=jumpy --opt-strategy=usc,11 --iter-configuration=tweety --iter-opt-strategy=bb,0 --iter-opt-heuristic=3 --iter-restart-on-model --quiet=1,0 example/cb-ctt/encoding/teaspoon.lp example/cb-ctt/instances/ITC-2007_asp/comp01.lp example/cb-ctt/instances/ud5.lp example/cb-ctt/configs/vg-random.lp
```

### heulingo with the ALNPS configuration Portfolio

```
heulingo --configuration=jumpy --opt-strategy=usc,11 --iter-configuration=tweety --iter-opt-strategy=bb,0 --iter-opt-heuristic=3 --iter-restart-on-model --quiet=1,0 example/cb-ctt/encoding/teaspoon.lp example/cb-ctt/instances/ITC-2007_asp/comp01.lp example/cb-ctt/instances/ud5.lp example/cb-ctt/configs/portfolio.lp
```

## ALNPS configurations

ALNPS configurations specify the behavior of the ALNPS heuristic,
especially for the destroy and prioritize operators.

### Special predicates

We introduce seven special predicates to specify ALNPS configurations in ASP programs.

- **`_project/2`** <br>
  is used to define sets of atoms that can serve as projected atoms,
  i.e., atoms that are subject to destruction and prioritization.

- **`_destroy/3`** and **`_destroy/2`** <br>
  are used to define possible behaviors of the destroy operator,
  specifying what parts of projected atoms can be destroyed and by what percentages (or how many).

- **`_prioritize/2`** and **`_prioritize/3`** <br>
  are used to define possible behaviors of the prioritize operator,
  specifying what parts of projected atoms can be prioritized and by what heuristic modifiers and values.

- **`_config/4`** <br>
  is used to define configurations, which are combinations of the projected atoms 
  and the behaviors of destroy and prioritize operators.

- **`_strategy/2`** <br>
  is used to define which configurations can be selected by which strategy.
  
### Examples

We present ALNPS configurations for the teaspoon encoding.
The goal in CB-CTT is to assign all lectures to timeslots and rooms
so that all hard constraints are satisfied and soft-constraint violations are minimized.
The teaspoon encoding uses two different atoms depending on constraints.
The atom `assigned(C,R,D,P)`, which represents that a lecture of a course `C`
is assigned to a room `R` at a period `P` on a day `D`,
is used to characterize a solution.
The atom `assigned(C,D,P)` omits the room information.

#### VG-Random

VG-Random randomly destroys parts of a current solution and
keeps the undestroyed part as much as possible in each iteration.
```asp
% example/cb-ctt/configs/vg-random.lp

_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).

_destroy((random,auto), assigned(C,R,D,P), (C,R,D,P)) :- assigned(C,R,D,P).
_destroy((random,auto), auto).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), 1, true).

_config("VG-Random", (assigned,4), (random,auto), (1,true)).

_strategy(roulette, "VG-Random").
```
The rule for `_project/2` means that the set `(assigned,4)` contains the atoms of `assigned/4` belonging to an answer set.
The rules for `_destroy/3` and `_destroy/2` mean that the destroy operator with behavior `(random,auto)` 
randomly selects terms from the third argument of `_destroy/3` and destroys the corresponding atoms of `assigned/4`, 
with an automatically computed percentage.
The rules for `_prioritize/2` and `_prioritize/3` mean that the prioritize operator with behavior `(1,true)` prioritizes 
the atoms of `assigned/4` in the undestroyed part, using clingo's heuristic statements with the modifier `true` and its value `1`. 
The rule for `_config/4` means that the configuration `"VG-Random"` uses the atoms in the set `(assigned,4)` as the projected atoms, 
assigns the behavior `(random,auto)` to the destroy operator, 
and assigns the behavior `(1,true)` to the prioritize operator. 
The rule for `_strategy/2` means that the roulette-wheel strategy (`roulette`) can select the configuration `"VG-Random"`.
Note that the current implementation of heulingo provides only `roulette` as the strategy.

#### Portfolio

Portfolio selects, in each iteration, one of the following configurations: 
Random 6%, Day-Period, Day-Room, Swap-Room 10%, and DP-Swap-Room 2.
```asp
% example/cb-ctt/configs/portfolio.lp

_project((assigned,4), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_project((assigned,3), assigned(C,D,P)) :- assigned(C,D,P).

_destroy((random,(6;10)), assigned(C,R,D,P), (C,R,D,P)) :- assigned(C,R,D,P).
_destroy((random,N), p(N)) :- N=(6;10).

_destroy((day_period,(1;2)), assigned(C,R,D,P), (D,P)) :- assigned(C,R,D,P).
_destroy((day_period,N), n(N)) :- N=(1;2).

_destroy((day_room,1), assigned(C,R,D,P), (D,R)) :- assigned(C,R,D,P).
_destroy((day_room,1), n(1)).

_prioritize((1,true), assigned(C,R,D,P)) :- assigned(C,R,D,P).
_prioritize((1,true), assigned(C,D,P)) :- assigned(C,D,P).
_prioritize((1,true), 1, true).

_config("Random 6%", (assigned,4), (random,6), (1,true)).

_config("Day-Period", (assigned,4), (day_period,1), (1,true)).

_config("Day-Room", (assigned,4), (day_room,1), (1,true)).

_config("Swap-Room 10%", (assigned,(4;3)), (random,10), (1,true)).

_config("DP-Swap-Room 2", (assigned,(4;3)), (day_period,2), (1,true)).

_strategy(roulette,C) :- _config(C,_,_,_).
```
The rules for `_project/2` define the atom sets `(assigned,4)` and `(assigned,3)`. 
The rules for `_destroy/3` and `_destroy/2` define the destroy operator behaviors `(random,6)`, `(random,10)`, `(day_period,1)`, `(day_period,2)`, and `(day_room,1)`.
Here, `p(N)` and `n(N)` represent the percentage and cardinality of destruction, respectively.
The rules for `_prioritize/2` and `_prioritize/3` define the prioritize operator behavior `(1,true)`. 
The rules for `_config/4` define the configurations `"Random 6%"`, `"Day-Period"`, `"Day-Room"`, `"Swap-Room 10%"`, and `"DP-Swap-Room 2"` 
by combining these atom sets and operator behaviors. 
For example, the fourth rule for `_config/4` means that the configuration `"Swap-Room 10%"` uses the atoms in `(assigned,4)` $\cup$ `(assigned,3)` as the projected atoms,
assigns the behavior `(random,10)` to the destroy operator,
and assigns the behavior `(1,true)` to the prioritize operator.
The rule for `_strategy/2` means that the roulette-wheel strategy can select all configurations defined in this ALNPS configuration.

## Known issues

- When solving problems that use lexicographic optimization, running heulingo with
  ```--iter-opt-mode=opt,N,dynamic,lt``` (where ```N``` $\leq$ 0) or
  ```--iter-opt-mode=opt,M,dynamic,leq``` (where ```M``` < 0)
  may result in incorrect optimal solutions.

## References

- [Large Neighborhood Prioritized Search for Combinatorial Optimization with Answer Set Programming](https://doi.org/10.24963/kr.2024/72),
  KR 2024 (CORE2023 Rank A*),
  Irumi Sugimori, Katsumi Inoue, Hidetomo Nabeshima, Torsten Schaub, Takehide Soh, Naoyuki Tamura, Mutsunori Banbara.
  [[repository](https://github.com/banbaralab/kr2024)]

- [ASP-Based Large Neighborhood Prioritized Search for Course Timetabling](https://doi.org/10.1007/978-3-031-74209-5_5),
  LPNMR 2024 (CORE2023 Rank B),
  Irumi Sugimori, Katsumi Inoue, Hidetomo Nabeshima, Torsten Schaub, Takehide Soh, Naoyuki Tamura, Mutsunori Banbara.
  [[repository](https://github.com/banbaralab/lpnmr2024)]


## sample sessions （a standard benchmark set）
---
- cb-ctt
```
heulingo --configuration=jumpy --opt-strategy=usc,11 --iter-configuration=tweety --iter-opt-strategy=bb,0 --iter-opt-heuristic=3 --iter-restart-on-model --init-cut-off-time=450 --iter-cut-off-time=6 --no-improvement-cutoff-threshold=2 --cut-off-time-increase-percent=5 --time-limit=3600 --quiet=1,0 example/cb-ctt/encoding/teaspoon.lp example/cb-ctt/instances/ITC-2007_asp/comp01.lp example/cb-ctt/instances/ud5.lp example/cb-ctt/configs/vg-random.lp
```

- pup
```
heulingo --opt-strategy=usc,3 --configuration=trendy --iter-opt-strategy=bb --init-cut-off-time=100 --iter-cut-off-time=2 --no-improvement-cutoff-threshold=2 --cut-off-time-increase-percent=5 --time-limit=600 --quiet=1,0 example/pup/encoding.lp example/pup/configs/vg-random.lp example/pup/show.lp example/pup/instances/07-partner_units_polynomial-28-0.asp
```
- sd 
```
heulingo --opt-strategy=usc,3 --configuration=handy --iter-opt-mode=opt,0,dynamic --init-cut-off-time=600 --iter-cut-off-time=60 --no-improvement-cutoff-threshold=2 --cut-off-time-increase-percent=5 --time-limit=3600 --quiet=1,0 example/sd/shift_design.lp example/sd/configs/vg-random.lp example/sd/instances/4_30m.lp
```
- sgp
```
heulingo --iter-opt-mode=opt,0,dynamic --init-cut-off-time=60 --iter-cut-off-time=6 --no-improvement-cutoff-threshold=2 --cut-off-time-increase-percent=5 --time-limit=1800 --quiet=1,0 example/sgp/golfer.lp example/sgp/configs/vg-random.lp example/sgp/instances/8.lp
```
- spg
```
heulingo --configuration=many -t4 --init-cut-off-time=20 --iter-cut-off-time=2 --no-improvement-cutoff-threshold=2 --cut-off-time-increase-percent=5 --time-limit=3600 --quiet=1,0 example/spg/sudoku.lp example/spg/configs/vg-random.lp example/spg/instances/9x9.lp
```
- tsp
```
heulingo --init-cut-off-time=10 --iter-cut-off-time=1 --no-improvement-cutoff-threshold=2 --cut-off-time-increase-percent=5 --time-limit=300 --quiet=1,0 example/tsp/tsp.lp example/tsp/configs/vg-random.lp example/tsp/instances/rand_70_300_1155482584_0.lp
```
- wsc
```
heulingo --opt-strat=usc,15 --iter-opt-strat=bb,0 --init-cut-off-time=600 --iter-cut-off-time=12 --no-improvement-cutoff-threshold=2 --cut-off-time-increase-percent=5 --time-limit=3600 --quiet=1,0 example/wsc/wsc.lp example/wsc/configs/vg-random.lp example/wsc/instances/wstratcomp_001.lp
```