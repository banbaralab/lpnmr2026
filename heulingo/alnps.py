from clingo.symbol import Function, Number, Symbol, SymbolType
from .logger import logger
import logging
import math
from .parser import ALNPSConfigParser
import random
from .solver import Result, Solution, Solver
from .strategy import Strategy
from .timer import Timer
from types import FrameType
from typing import Any

class ALNPS:
    """
    Implementation of Adaptive Large Neighborhood Prioritized Search (ALNPS).

    :param solver: ASP solver object.
    :type solver: Solver
    :param strategies: Dictionary mapping strategy names to strategy objects.
    :type strategies: dict[str, Strategy]
    :param default_strategy_name: Name of strategy to use when not specified. Defaults to "roulette".
    :type default_strategy_name: str, optional
    :param stats_history_size: Maximum number of recent iteration stats to retain. Defaults to 1.
    :type stats_history_size: int, optional
    """
    def __init__(self, solver: Solver, strategies: dict[str, Strategy], default_strategy_name: str = "roulette", stats_history_size: int = 1):
        self._solver = solver
        self._strategies = strategies
        self._default_strategy_name = default_strategy_name
        self._stats_history_size = stats_history_size
        self._timer = Timer()

    def handler(self, signum: int, frame: FrameType | None) -> None:
        """
        Signal handler that interrupts solver.

        :param signum: Signal number.
        :type signum: int
        :param frame: Current stack frame or None.
        :type frame: FrameType | None
        """
        self._solver.interrupt()

    def _read_alnps_config(self, solution: Solution) -> tuple[dict[str, Any], Strategy]:
        """
        Parse ALNPS configuration from solution.

        :param solution: Solution object.
        :type solution: Solution
        :return: ALNPS configuration and selected strategy.
        :rtype: tuple[dict[str, Any], Strategy]
        """
        alnps_config = ALNPSConfigParser.get_alnps_config(solution, list(self._strategies.keys()), self._default_strategy_name)
        strategy = self._strategies[alnps_config["strategy"]]
        return alnps_config, strategy

    def _generate_heuristic_subprogram(self, alnps_config: dict[str, Any]) -> str:
        """
        Generate #heuristic statements for LNPS and integrity constraints for LNS 
        from predicate signatures of projected atoms.

        :param alnps_config: ALNPS configuration dictionary.
        :type alnps_config: dict[str, Any]
        :return: #heuristic statements and integrity constraints.
        :rtype: str
        """
        heuristic_subprogram = ""
        for signature in alnps_config["projected_signatures"]:
            name = signature["name"]
            args = ",".join(["X"+str(i) for i in range(signature["arity"])])
            atom = f"{name}({args})"
            heuristic_subprogram += (
                f"#heuristic {atom} : __heuristic({atom},W,M,t), W != inf. [W,M]"
                f":- not {atom}, __heuristic({atom},inf,true,t)."
                f":- {atom}, __heuristic({atom},inf,false,t)."
            )
        return heuristic_subprogram

    def _is_stop_criterion_met(self, best_solution: Solution, result: Result, bound: list[int], valiability: bool) -> bool:
        """
        Check if stop criterion is met.

        :param best_solution: Current Best solution.
        :type best_solution: Solution
        :param result: Result of last solver run.
        :type result: Result
        :param bound: Initial bound for objective function(s) used in last solver run.
        :type bound: list[int]
        :param valiability: Whether current LNPS configuration has variability.
        :type valiability: bool
        :return: True if stop criterion is met, False otherwise.
        :rtype: bool
        """
        if (
            best_solution is None
            or self._solver.is_interrupted
            or (result == Result.OPTIMUM_FOUND and valiability)
        ):
            return True
        
        if bound is not None:
            if (
                result == Result.UNSAT 
                and bound[:-1] == best_solution.cost[:-1] 
                and bound[-1] == best_solution.cost[-1] - 1
                and valiability
            ):
                return True

        return False

    def _has_variability(self, lnps_config: dict[str, Any]) -> bool:
        """
        Check if LNPS configuration includes no prioritize operator using level inf.

        :param lnps_config: LNPS configuration.
        :type lnps_config: dict[str, Any]
        :return: True if LNPS configuration has variability, False otherwise.
        :rtype: bool
        """
        for prioritize_operator in lnps_config["prioritize_operators"]:
            if prioritize_operator["value"] == "inf":
                return False
        return True

    def _format_atoms(self, atoms: set[Symbol]) -> str:
        """
        Format list of atoms into sorted space-separated string.

        :param atoms: List of atoms.
        :type atoms: list[Symbol]
        :return: Formatted atom string.
        :rtype: str
        """
        return " ".join([str(atom) for atom in sorted(atoms)])

    def _project(self, solution: Solution, lnps_config: dict[str, Any]) -> set[Symbol]:
        """
        Get atoms subject to LNPS from current solution.

        :param solution: Current solution.
        :type solution: Solution
        :param lnps_config: LNPS configuration.
        :type lnps_config: dict[str, Any]
        :return: Projected atoms.
        :rtype: set[Symbol]
        """
        projected_atoms = set()

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Current solution:", solution)
            logger.debug("Current solution cost:", *solution.cost)

        for project_operator_name in lnps_config["project_operators"]:
            projected_atoms.update(ALNPSConfigParser.get_projected_atoms(solution, project_operator_name))

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(len(projected_atoms), "projected atoms:", self._format_atoms(projected_atoms))

        return projected_atoms

    def _destroy_atoms_if_term_selected(self, atom_term_pairs: list[dict[str, Symbol]], percent_or_number: dict[str, Any]) -> set[Symbol]:
        """
        Randomly select terms by given percentage (or number) 
        and return all atoms corresponding to selected terms.

        :param atom_term_pairs: Atoms subject to destruction and corresponding terms.
        :type atom_term_pairs: list[dict[str, Symbol]]
        :param percent_or_number: What percentage (or how many) terms are selected by.
        :type percent_or_number: dict[str, Any]
        :return: Destroyed atoms.
        :rtype: set[Symbol]
        """
        candidate_terms = set()
        for pair in atom_term_pairs:
            candidate_terms.add(pair["term"])

        destroyed_atoms = set()
        value = percent_or_number["value"]
        if percent_or_number["type"] == "p":
            num_selected_terms = round(len(candidate_terms) * value / 100)
        else:
            num_selected_terms = min(len(candidate_terms), value)
        selected_terms = random.sample(sorted(candidate_terms), num_selected_terms)
        for pair in atom_term_pairs:
            if pair["term"] in selected_terms:
                destroyed_atoms.add(pair["atom"])

        return destroyed_atoms

    def _is_tuple(self, term: Symbol) -> bool:
        """
        Check if given term is tuple.

        :param term: Term.
        :type term: Symbol
        :return: True if given term is tuple, False otherwise.
        :rtype: bool
        """
        return term.type == SymbolType.Function and not term.name

    def _destroy_atoms_if_all_args_selected(self, atom_term_pairs: list[dict[str, Symbol]], percents_or_numbers: list[dict[str, Any]]) -> set[Symbol]:
        """
        Randomly select arguments by given percentages (or numbers) 
        and return all atoms corresponding to terms whose all arguments are selected.

        :param atom_term_pairs: Atoms subject to destruction and corresponding terms.
        :type atom_term_pairs: list[dict[str, Symbol]]
        :param percents_or_numbers: What percentages (or how many) arguments are selected by.
        :type percents_or_numbers: list[dict[str, Any]]
        :return: Destroyed atoms.
        :rtype: set[Symbol]
        """
        candidate_args = [set() for i in range(len(percents_or_numbers))]
        selected_args = []

        for pair in atom_term_pairs:
            if self._is_tuple(pair["term"]) and len(pair["term"].arguments) == len(percents_or_numbers):
                for i, arg in enumerate(pair["term"].arguments):
                    candidate_args[i].add(arg)

        destroyed_atoms = set()
        for i, pn in enumerate(percents_or_numbers):
            value = pn["value"]
            if pn["type"] == "p":
                num_selected_args = round(len(candidate_args[i]) * value / 100)
            else:
                num_selected_args = min(len(candidate_args[i]), value)
            selected_args.append(random.sample(sorted(candidate_args[i]), num_selected_args))
        for pair in atom_term_pairs:
            if self._is_tuple(pair["term"]) and len(pair["term"].arguments) == len(percents_or_numbers):
                all_args_selected = all(
                    arg in selected_args[i]
                    for i, arg in enumerate(pair["term"].arguments)
                )
                if all_args_selected:
                    destroyed_atoms.add(pair["atom"])

        return destroyed_atoms

    def _destroy(self, solution: Solution, projected_atoms: set[Symbol], lnps_config: dict[str, Any]) -> set[Symbol]:
        """
        Randomly select destroyed atoms and return undestroyed atoms.

        :param solution: Current solution.
        :type solution: Solution
        :param projected_atoms: Projected atoms.
        :type projected_atoms: set[Symbol]
        :param lnps_config: LNPS configuration.
        :type lnps_config: dict[str, Any]
        :return: Undestroyed atoms.
        :rtype: set[Symbol]
        """
        destroyed_atoms = set()
        for destroy_operator in lnps_config["destroy_operators"]:
            atom_term_pairs = ALNPSConfigParser.get_atom_term_pairs(solution, projected_atoms, destroy_operator["name"])
            if len(destroy_operator["percents_or_numbers"]) == 1:
                destroyed_atoms.update(self._destroy_atoms_if_term_selected(atom_term_pairs, destroy_operator["percents_or_numbers"][0]))
            else:
                destroyed_atoms.update(self._destroy_atoms_if_all_args_selected(atom_term_pairs, destroy_operator["percents_or_numbers"]))

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(len(destroyed_atoms), "destroyed atoms:", self._format_atoms(destroyed_atoms))

        undestroyed_atoms = projected_atoms - destroyed_atoms

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(len(undestroyed_atoms), "undestroyed atoms:", self._format_atoms(undestroyed_atoms))

        return undestroyed_atoms

    def _prioritize(self, solution: Solution, undestroyed_atoms: set[Symbol], lnps_config: dict[str, Any], iteration: int) -> set[Symbol]:
        """
        Generate external atoms of __heuristic/4 for undestroyed atoms.

        :param solution: Current solution.
        :type solution: Solution
        :param undestroyed_atoms: Undestroyed atoms.
        :type undestroyed_atoms: set[Symbol]
        :param lnps_config: LNPS configuration.
        :type lnps_config: dict[str, Any]
        :param iteration: Number of iterations.
        :type iteration: int
        :return: External atoms of __heuristic/4.
        :rtype: set[Symbol]
        """
        prioritized_atoms = set()
        external_atoms = set()

        for prioritize_operator in lnps_config["prioritize_operators"]:
            heuristic_targets = ALNPSConfigParser.get_heuristic_targets(solution, undestroyed_atoms, prioritize_operator["name"])
            for target in heuristic_targets:
                prioritized_atoms.add(target)
                if prioritize_operator["value"] == "inf":
                    value = Function("inf")
                else:
                    value = Number(prioritize_operator["value"])
                external_atoms.add(
                    Function(
                        "__heuristic",
                        [
                            target,
                            value,
                            Function(prioritize_operator["modifier"]),
                            Number(iteration)
                        ]
                    )
                )

        for atom in undestroyed_atoms - prioritized_atoms:
            external_atoms.add(
                Function(
                    "__heuristic",
                    [atom, Number(1), Function("true"), Number(iteration)]
                )
            )

        return external_atoms

    def _generate_external_statements(self, external_atoms: set[Symbol]) -> str:
        """
        Generate #external statements for given atoms.

        :param external_atoms: External atoms.
        :type external_atoms: set[Symbol]
        :return: #external statements.
        :rtype: str
        """
        external_statements = ""
        for atom in external_atoms:
            external_statements += f"#external {atom}."
        return external_statements

    def _compute_bound(self, solution: Solution, params: dict[str, Any]) -> list[int]:
        """
        Compute initial bound for objective function(s) used in next solver run.

        :param solution: Current solution.
        :type solution: Solution
        :param params: Bound computation parameters.
        :type params: dict[str, Any]
        :return: Computed bound.
        :rtype: list[int]
        """
        if params["dynamic"]:
            bound = solution.cost[:-1]
            final_cost = solution.cost[-1]
            if params["lt"]:
                bound.append(math.ceil(final_cost + abs(final_cost) * params["percent"] / 100) - 1)
            else:
                bound.append(math.floor(final_cost + abs(final_cost) * params["percent"] / 100))
            return bound
        else:
            return params["bound"]
    
    def _update_best_solution(self, best_solution: Solution, new_solution: Solution | None) -> Solution:
        """
        Update current best solution if new one is better.

        :param best_solution: Current best solution.
        :type best_solution: Solution
        :param new_solution: New solution.
        :type new_solution: Solution | None
        :return: Updated current best solution.
        :rtype: Solution
        """
        if new_solution is not None and new_solution.cost < best_solution.cost:
            new_best_solution = new_solution
        else:
            new_best_solution = best_solution
        return new_best_solution

    def _update_no_improvement_cutoff_count(self, no_improvement_cutoff_count: int, best_solution: Solution, new_solution: Solution | None, result: Result) -> int:
        """
        Update count of consecutive iterations without improvement.

        :param no_improvement_cutoff_count: Current count.
        :type no_improvement_cutoff_count: int
        :param best_solution: Current best solution.
        :type best_solution: Solution
        :param new_solution: New solution.
        :type new_solution: Solution | None
        :param result: Result of last solver run.
        :type result: Result
        :return: Updated count.
        :rtype: int
        """
        if result in [Result.UNSAT, Result.OPTIMUM_FOUND]:
            new_no_improvement_cutoff_count = no_improvement_cutoff_count
        elif result == Result.SAT and new_solution.cost < best_solution.cost:
            new_no_improvement_cutoff_count = 0
        else:
            new_no_improvement_cutoff_count = no_improvement_cutoff_count + 1
        return new_no_improvement_cutoff_count

    def _update_stats(self, stats: list[dict[str, Any]], iteration_info: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Update statistics with current iteration information.

        :param stats: List of statistics dictionaries with the following keys:
            - "current_solution" (Solution | None): Current solution; None only for statistics of initial solution search.
            - "projected_atoms" (set[Symbol] | None): Projected atoms in current iteration; None only for statistics of initial solution search.
            - "destroyed_atoms" (set[Symbol] | None): Destroyed atoms in current iteration; None only for statistics of initial solution search.
            - "undestroyed_atoms" (set[Symbol] | None): Undestroyed atoms in current iteration; None only for statistics of initial solution search.
            - "new_solution" (Solution | None): New solution found in current iteration, or None if no solution found.
            - "best_solution" (Solution): Current best solution.
            - "no_improvement_cutoff_count" (int): Current count of consecutive iterations without improvement.
            - "time_to_last_solution" (float): Time taken to find last solution in current iteration.
            - "elapsed_time" (float): Elapsed time since start of ALNPS.
        :type stats: list[dict[str, Any]]
        :param iteration_info: Current iteration information dictionary with the following keys:
            - "initial_solution" (Solution): Initial solution; only present in information for initial solution search.
            - "current_solution" (Solution): Current solution; only present in information for searches within iterations.
            - "projected_atoms" (set[Symbol]): Projected atoms in current iteration; only present in information for searches within iterations.
            - "undestroyed_atoms" (set[Symbol]): Undestroyed atoms in current iteration; only present in information for searches within iterations.
            - "new_solution" (Solution | None): New solution found in current iteration, or None if no solution found; only present in information for searches within iterations.
            - "search_stats" (dict[str, Any]): Search statistics dictionary with the following keys:
                - "result" (Result): Result of last solver run.
                - "time_to_last_solution" (float): Time taken to find last solution in current iteration.
        :type iteration_info: dict[str, Any]
        :return: Updated statistics.
        :rtype: list[dict[str, Any]]
        """
        if not stats:
            new_stats = [
                {
                    "current_solution": None,
                    "projected_atoms": None,
                    "destroyed_atoms": None,
                    "undestroyed_atoms": None,
                    "new_solution": iteration_info["initial_solution"],
                    "best_solution": iteration_info["initial_solution"],
                    "no_improvement_cutoff_count": 0,
                }
            ]
        else:
            new_stats = stats.copy()
            result = iteration_info["search_stats"]["result"] 
            best_solution = stats[-1]["best_solution"]
            new_solution = iteration_info["new_solution"]

            new_stats.append(
                {
                    "current_solution": iteration_info["current_solution"],
                    "projected_atoms": iteration_info["projected_atoms"],
                    "destroyed_atoms": iteration_info["projected_atoms"] - iteration_info["undestroyed_atoms"],
                    "undestroyed_atoms": iteration_info["undestroyed_atoms"],
                    "new_solution": new_solution,
                    "best_solution": self._update_best_solution(best_solution, new_solution),
                    "no_improvement_cutoff_count": self._update_no_improvement_cutoff_count(stats[-1]["no_improvement_cutoff_count"], best_solution, new_solution, result),
                }
            )

        new_stats[-1]["time_to_last_solution"] = iteration_info["search_stats"]["time_to_last_solution"]
        new_stats[-1]["elapsed_time"] = self._timer.elapsed()

        if len(new_stats) > self._stats_history_size:
            del new_stats[0]

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Best solution:", new_stats[-1]["best_solution"])
            logger.debug("Best solution cost:", *new_stats[-1]["best_solution"].cost)

        return new_stats

    def _accept(self, new_solution: Solution, current_solution: Solution) -> bool:
        """
        Evaluate new solution whether or not it becomes new current solution.

        :param new_solution: New solution.
        :type new_solution: Solution
        :param current_solution: Current solution.
        :type current_solution: Solution
        :return: True if new solution is accepted as current solution, False otherwise.
        :rtype: bool
        """
        return new_solution.cost < current_solution.cost

    def _update_cutoff(self, cut_off_time: float, stats: dict[str, Any], params: dict[str, int]) -> float:
        """
        Increase cut-off-time if necessary.

        :param cut_off_time: Current cut-off-time.
        :type cut_off_time: float
        :param stats: Statistics.
        :type stats: dict[str, Any]
        :param params: Cut-off-time update parameters.
        :type params: dict[str, int]
        :return: Updated cut-off-time.
        :rtype: float
        """
        if (
            stats[-1]["no_improvement_cutoff_count"] != 0
            and stats[-1]["no_improvement_cutoff_count"] % params["no_improvement_cutoff_threshold"] == 0 
        ):
            return cut_off_time + cut_off_time * params["cut_off_time_increase_percent"] / 100
        else:
            return cut_off_time

    def _print_result(self, best_solution: Solution, iterations: int) -> None:
        """
        Print final result and summary.

        :param best_solution: Current best solution.
        :type best_solution: Solution
        :param iterations: Number of iterations.
        :type iterations: int
        """
        logger.info(f"---- [ Result ] ---------------------------------------------------------------------------")
        if best_solution is None:
            if self._solver.is_interrupted:
                logger.solution("UNKNOWN")
            else:
                logger.solution("UNSATISFIABLE")
        else:
            logger.variable("Answer:", best_solution)
            if self._solver.is_interrupted:
                logger.solution("SATISFIABLE")
            else:
                logger.solution("OPTIMUM FOUND")
            logger.answer("Optimization:", *best_solution.cost)
        logger.info("Iterations:", iterations)

    def main(self, files: list[str], params: dict[str, Any], context: Any) -> None:
        """
        Run Adaptive Large Neighborhood Prioritized Search (ALNPS).

        :param files: Problem instance, ASP encoding, and ALNPS configuration.
        :type files: list[str]
        :param params: Dictionary containing ALNPS parameters.
        :type params: dict[str, Any]
        :param context: Context object whose methods are called during grounding using @-syntax.
        :type context: Any
        """
        iteration = 0
        stats = []
        bound = None
        variability = True

        self._solver.read(files)
        self._solver.ground([("base", [])], context)

        # Search for an initial solution
        logger.info(f"---- [ Finding an initial solution ] ------------------------------------------------------")
        solution, search_stats = self._solver.search(params["init_cut_off_time"], True)

        if self._is_stop_criterion_met(solution, search_stats["result"], bound, variability):
            self._print_result(solution, iteration)
            return

        best_solution = solution
        stats = self._update_stats(stats, {"initial_solution": solution, "search_stats": search_stats})
        cut_off_time = params["iter_cut_off_time"]

        alnps_config, strategy = self._read_alnps_config(solution)
        lnps_config = strategy.get_initial_config(alnps_config, solution)

        # Generate heuristic statements
        heuristic_subprogram = self._generate_heuristic_subprogram(alnps_config)
        self._solver.add("heuristic", ["t"], heuristic_subprogram)

        prev_external_atoms = []

        self._solver.set_solver_config(params["iter_solver_config"])

        while not self._is_stop_criterion_met(best_solution, search_stats["result"], bound, variability):
            iteration += 1
            logger.info(f"---- [ Iteration {iteration} ] ------------------------------------------------------------")

            variability = self._has_variability(lnps_config)

            projected_atoms = self._project(solution, lnps_config)
            undestroyed_atoms = self._destroy(solution, projected_atoms, lnps_config)
            external_atoms = self._prioritize(solution, undestroyed_atoms, lnps_config, iteration)

            # Deactivate heuristic statements in previous iteration
            self._solver.release_external(prev_external_atoms)

            external_statements = self._generate_external_statements(external_atoms)
            self._solver.add("external", ["t"], external_statements)
            self._solver.ground([("external", [Number(iteration)])])
            self._solver.ground([("heuristic", [Number(iteration)])])

            # Activate heuristic statements for undestroyed part
            self._solver.assign_external(external_atoms, True)

            prev_external_atoms = external_atoms.copy()

            if params["is_cost_bounded"]:
                bound = self._compute_bound(solution, params["bound_params"])
                self._solver.add_bound(bound)

            # Prioritized search for new solution
            temp_solution, search_stats = self._solver.search(cut_off_time, False)
            
            stats = self._update_stats(
                stats, 
                {
                    "current_solution": solution, 
                    "projected_atoms": projected_atoms, 
                    "undestroyed_atoms": undestroyed_atoms,
                    "new_solution": temp_solution,
                    "search_stats": search_stats
                }
            )

            if temp_solution is not None:
                if self._accept(temp_solution, solution):
                    solution = temp_solution
                if temp_solution.cost < best_solution.cost:
                    best_solution = temp_solution

            cut_off_time = self._update_cutoff(cut_off_time, stats, params["update_cutoff_params"])

            lnps_config = strategy.update_config(lnps_config, alnps_config, stats)

        self._print_result(best_solution, iteration)