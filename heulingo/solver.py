from abc import ABC, abstractmethod
from clingo.ast import AST, ASTType, parse_files, parse_string, ProgramBuilder
from clingo.control import Control
from clingo.solving import Model, SolveHandle, SolveResult
from clingo.statistics import StatisticsMap
from clingo.symbol import Function, Number, Symbol
from clingo.theory import Theory
from enum import Enum
import importlib.util
from .logger import logger
import logging
from .timer import Timer
from typing import Any

if importlib.util.find_spec("clingodl"):
    from clingodl import ClingoDLTheory
if importlib.util.find_spec("clingcon"):
    from clingcon import ClingconTheory

class Result(Enum):
    """
    Result of solver run.
    """
    UNKNOWN = 0
    SAT = 1
    UNSAT = 2
    OPTIMUM_FOUND = 3

class Solution:
    """
    Solution found by solver.

    :param shown: Atoms and terms as outputted by clingo.
    :type shown: list[Symbol]
    :param true: Atoms in model.
    :type true: list[Symbol]
    :param cost: List of integer cost values of model.
    :type cost: list[int]
    """
    def __init__(self, shown: list[Symbol], true: list[Symbol], cost: list[int]):
        self._shown = set(shown)
        self._true = set(true)
        self._cost = cost

    def __str__(self) -> str:
        """
        Return string representation of solution.

        :return: Space-separated string of atoms and terms as outputted by clingo.
        :rtype: str
        """
        return " ".join([str(symbol) for symbol in sorted(self._shown)])

    @property
    def shown(self) -> set[Symbol]:
        """
        Get atoms and terms as outputted by clingo.

        :return: Atoms and terms as outputted by clingo.
        :rtype: set[Symbol]
        """
        return self._shown
    
    @property
    def true(self) -> set[Symbol]:
        """
        Get atoms in model.

        :return: Atoms in model.
        :rtype: set[Symbol]
        """
        return self._true    
    
    @property
    def cost(self) -> list[int]:
        """
        Get list of integer cost values of model.

        :return: List of integer cost values of model.
        :rtype: list[int]
        """
        return self._cost

class Solver(ABC):
    """
    Solver.

    :param ctl: Control object for grounding/solving process.
    :type ctl: Control
    """
    def __init__(self, ctl: Control):
        self._ctl = ctl
        self._is_interrupted = False

        self._print_solver_config()

    @property
    def is_interrupted(self):
        """
        Check if search is interrupted.

        :return: True if search is interrupted, False otherwise.
        :rtype: _type_
        """
        return self._is_interrupted

    @abstractmethod
    def read(self, files: list[str]) -> None:
        """
        Abstract method to read problem instance, ASP encoding, ALNPS configuration, etc.

        :param files: Input files.
        :type files: list[str]
        """
        pass

    def ground(self, parts: list[tuple[str, list[Symbol]]], context: Any = None) -> None:
        """
        Ground given program parts.

        :param parts: Program names and program arguments to ground.
        :type parts: list[tuple[str, list[Symbol]]]
        :param context: Context object whose methods are called during grounding using @-syntax. Defaults to None.
        :type context: Any
        """
        self._ctl.ground(parts, context)

    def add(self, name: str, parameters: list[str], program: str) -> None:
        """
        Add given program to specified program block.

        :param name: Name of program block to add.
        :type name: str
        :param parameters: Parameters of program block to add.
        :type parameters: list[str]
        :param program: Non-ground program in string form.
        :type program: str
        """
        self._ctl.add(name, parameters, program)

    def _print_solver_config(self):
        """
        Print values of some solver's options.
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"--configuration={self._ctl.configuration.configuration}")
            logger.debug(f"--opt-strategy={self._ctl.configuration.solver.opt_strategy}")
            logger.debug(f"--opt-heuristic={self._ctl.configuration.solver.opt_heuristic}")
            if int(self._ctl.configuration.solver.restart_on_model):
                logger.debug("--restart-on-model")
            else:
                logger.debug("--no-restart-on-model")
            logger.debug(f"--heuristic={self._ctl.configuration.solver.heuristic}")

    def set_solver_config(self, solver_config: dict[str, str]) -> None:
        """
        Configure solver with given settings.

        :param solver_config: Settings of solver's options.
        :type solver_config: dict[str, str]
        """
        if "configuration" in solver_config:
            self._ctl.configuration.configuration = solver_config["configuration"]
        if "opt_strategy" in solver_config:
            self._ctl.configuration.solver.opt_strategy = solver_config["opt_strategy"]
        if "opt_heuristic" in solver_config:
            self._ctl.configuration.solver.opt_heuristic = solver_config["opt_heuristic"]
        if "restart_on_model" in solver_config:
            self._ctl.configuration.solver.restart_on_model = solver_config["restart_on_model"]
        if "heuristic" in solver_config:
            self._ctl.configuration.solver.heuristic = solver_config["heuristic"]
        if "opt_mode" in solver_config:
            self._ctl.configuration.solve.opt_mode = solver_config["opt_mode"]

        self._print_solver_config()

    def release_external(self, external_atoms: list[Symbol]) -> None:
        """
        Release external atoms.

        :param external_atoms: External atoms.
        :type external_atoms: list[Symbol]
        """
        for external_atom in external_atoms:
            self._ctl.release_external(external_atom)

    def assign_external(self, external_atoms: list[Symbol], truth: bool) -> None:
        """
        Assign truth value to external atoms.

        :param external_atoms: External atoms.
        :type external_atoms: list[Symbol]
        :param truth: Truth value.
        :type truth: bool
        """
        for external_atom in external_atoms:
            self._ctl.assign_external(external_atom, truth)

    @abstractmethod
    def add_bound(self, bound: list[int]) -> None:
        """
        Abstract method to add initial bound for objective function(s).

        :param bound: Initial bound for objective function(s).
        :type bound: list[int]
        """
        pass

    @abstractmethod
    def search(self, cut_off_time: float, require_solution: bool) -> tuple[Solution, dict[str, Any]]:
        """
        Abstract method to search for new solution.

        :param cut_off_time: Cut-off-time.
        :type cut_off_time: float
        :param require_solution: Whether any solution is required.
        :type require_solution: bool
        :return: Last solution and statistics.
        :rtype: tuple[Solution, dict[str, Any]]
        """
        pass

    def interrupt(self):
        """
        Interrupt search.
        """
        self._is_interrupted = True
        self._ctl.interrupt()

class Clingo(Solver):
    """
    clingo.

    :param ctl: Control object for grounding/solving process.
    :type ctl: Control
    """
    def __init__(self, ctl: Control):
        super().__init__(ctl)
        self._cut_off_timer = Timer()
        self._search_timer = Timer()
        self._last_solution = None
        self._stats = {}
        self._is_cutoff = False

    def read(self, files: list[str]) -> None:
        """
        Load input files.

        :param files: Input files.
        :type files: list[str]
        """
        for file in files:
            self._ctl.load(file)

    def add_bound(self, bound: list[int]) -> None:
        """
        Add initial bound for objective function(s) to clingo's option --opt-mode.

        :param bound: Initial bound for objective function(s).
        :type bound: list[int]
        """
        mode = self._ctl.configuration.solve.opt_mode.split(",")[0]
        self._ctl.configuration.solve.opt_mode = mode + "," + ",".join([str(cost) for cost in bound])
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Bound:", *bound)

    def _on_model_callback(self, model: Model) -> None:
        """
        Callback for intercepting models.
        Update last solution and restart timer to measure time since last solution.

        :param model: Model object.
        :type model: Model
        """
        self._last_solution = Solution(
            model.symbols(shown=True),
            model.symbols(atoms=True),
            model.cost
        )
        self._cut_off_timer.restart()
        self._stats["time_to_last_solution"] = self._search_timer.elapsed()

    def _on_statistics_callback(self, step: StatisticsMap, accu: StatisticsMap) -> None:
        """
        Callback to update statistics.

        :param step: Map for per step statistics.
        :type step: StatisticsMap
        :param accu: Map for accumulated statistics.
        :type accu: StatisticsMap
        """
        pass

    def _on_finish_callback(self, ret: SolveResult) -> None:
        """
        Callback called once search has finished.
        Determine result of search.

        :param ret: Result of solve call.
        :type ret: SolveResult
        """
        if ret.satisfiable:
            self._stats["result"] = Result.SAT

        if (ret.exhausted and not self._is_interrupted and not self._is_cutoff):
            if ret.unsatisfiable:
                self._stats["result"] = Result.UNSAT
            else:
                self._stats["result"] = Result.OPTIMUM_FOUND

    def _cutoff(self, handle: SolveHandle, cut_off_time: float, require_solution: bool) -> None:
        """
        Cut off search if time since last solution (or start) exceeds cut-off-time.

        :param handle: Handle for solve call.
        :type handle: SolveHandle
        :param cut_off_time: Cut-off-time.
        :type cut_off_time: float
        :param require_solution: Whether any solution is required.
        :type require_solution: bool
        """
        if require_solution and self._last_solution is None:
            return
        if not self._is_cutoff and cut_off_time < self._cut_off_timer.elapsed():
            self._is_cutoff =True
            handle.cancel()

    def search(self, cut_off_time: float, require_solution: bool) -> tuple[Solution, dict[str, Any]]:
        """
        Search for new solution with clingo.

        :param cut_off_time: Cut-off-time.
        :type cut_off_time: float
        :param require_solution: Whether any solution is required.
        :type require_solution: bool
        :return: Last solution and statistics.
        :rtype: tuple[Solution, dict[str, Any]]
        """
        self._last_solution = None
        self._stats = {"result": Result.UNKNOWN, "time_to_last_solution": None}
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Cut-off-time:", cut_off_time)
        self._search_timer.restart()

        with self._ctl.solve(
            on_model=self._on_model_callback, 
            on_statistics=self._on_statistics_callback,
            on_finish=self._on_finish_callback,
            async_=True
        ) as handle:
            self._cut_off_timer.restart()
            self._is_cutoff = False
            while not handle.wait(0):
                self._cutoff(handle, cut_off_time, require_solution)

        return self._last_solution, self._stats

class ClingoTheory(Clingo):
    """
    clingo with Theory object.

    :param ctl: Control object for grounding/solving process.
    :type ctl: Control
    :param thy: Theory object.
    :type thy: Theory
    """
    def __init__(self, ctl: Control, thy: Theory):
        super().__init__(ctl)
        self._thy = thy
        self._bound_step = 1
        self._prev_bound_atom = None

    def _read_asts(self, asts: list[AST]) -> None:
        """
        Read asts of input files.

        :param asts: AST objects.
        :type asts: list[AST]
        """
        pass

    def read(self, files: list[str]) -> None:
        """
        Load input files for solver using Theory object.

        :param files: Input files.
        :type files: list[str]
        """
        self._thy.register(self._ctl)
        asts = []
        with ProgramBuilder(self._ctl) as pb:
            def callback(ast):
                asts.append(ast)
                self._thy.rewrite_ast(ast, pb.add)
            parse_files(files, callback)
        self._read_asts(asts)
        
    def _on_model_callback(self, model: Model) -> None:
        """
        Callback for intercepting models.
        Inform theory that model has been found and call parent method.

        :param model: Model found by clingo.
        :type model: Model
        """
        self._thy.on_model(model)
        super()._on_model_callback(model)

    def _on_statistics_callback(self, step: StatisticsMap, accu: StatisticsMap) -> None:
        """
        Callback to update statistics.
        Add theory's statistics to given maps and call parent method.

        :param step: Map for per step statistics.
        :type step: StatisticsMap
        :param accu: Map for accumulated statistics.
        :type accu: StatisticsMap
        """
        self._thy.on_statistics(step, accu)
        super()._on_statistics_callback(step, accu)

    def search(self, cut_off_time: float, require_solution: bool) -> tuple[Solution, dict[str, Any]]:
        """
        Search for new solution with solver using Theory object.

        :param cut_off_time: Cut-off-time.
        :type cut_off_time: float
        :param require_solution: Whether any solution is required.
        :type require_solution: bool
        :return: Last solution and statistics.
        :rtype: tuple[Solution, dict[str, Any]]
        """
        self._thy.prepare(self._ctl)
        return super().search(cut_off_time, require_solution)
    
    def _add_bound_subprogram(self, bound_subprogram: str) -> None:
        """
        Add subprogram bound(t) to program.

        :param bound_subprogram: Constraint to set bound for objective function.
        :type bound_subprogram: str
        """
        with ProgramBuilder(self._ctl) as pb:
            parse_string(f"#program bound(t). {bound_subprogram}", lambda ast: self._thy.rewrite_ast(ast, pb.add))

    def _add_bound_atom(self, bound: list[int]) -> None:
        """
        Add atom of __b/2 to set bound for objective function.

        :param bound: Bound for objective function.
        :type bound: list[int]
        """
        if self._prev_bound_atom is not None:
            self._ctl.release_external(self._prev_bound_atom)
        bound_atom = Function("__b", [Number(bound[0]), Number(self._bound_step)])
        self._ctl.add("bound", ["t"], f"#external {bound_atom}.")
        self._ctl.ground([("bound", [Number(self._bound_step)])])
        self._ctl.assign_external(bound_atom, True)
        self._prev_bound_atom = bound_atom
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Bound:", *bound)

if importlib.util.find_spec("clingodl"):
    class ClingoDL(ClingoTheory):
        """
        clingo-dl.

        :param ctl: Control object for grounding/solving process.
        :type ctl: Control
        """
        def __init__(self, ctl: Control):
            super().__init__(ctl, ClingoDLTheory())

    class ClingoDLMinimizeVariable(ClingoDL):
        """
        clingo-dl with --minimize-variable.

        :param ctl: Control object for grounding/solving process.
        :type ctl: Control
        :param minimize_variable: Variable for clingo-dl's option --minimize-variable.
        :type minimize_variable: Symbol
        """
        def __init__(self, ctl: Control, minimize_variable: Symbol):
            super().__init__(ctl)
            self._minimize_variable = minimize_variable

        def read(self, files: list[str]) -> None:
            """
            Call parent method
            and add difference constraint to set bound for objective function.

            :param files: Input files.
            :type files: list[str]
            """
            super().read(files)
            self._add_bound_subprogram(f"&diff {{ {self._minimize_variable} - 0 }} <= B :- __b(B,t).")

        def add_bound(self, bound: list[int]) -> None:
            """
            Add bound for objective function by adding atom of __b/2.

            :param bound: Bound for objective function.
            :type bound: list[int]
            """
            self._add_bound_atom(bound)

        def _on_model_callback(self, model: Model):
            """
            Callback for intercepting models.
            Extract value assigned to variable to minimize,
            update last solution, and restart timer to measure time since last solution.

            :param model: Model object.
            :type model: Model
            """
            self._thy.on_model(model)
            for var, val in self._thy.assignment(model.thread_id):
                if var == self._minimize_variable:
                    self._last_solution = Solution(
                        model.symbols(shown=True),
                        model.symbols(atoms=True),
                        [int(val)]
                    )
                    break   
            logger.info("Optimization:", *self._last_solution.cost)
            self._cut_off_timer.restart()
            self._stats["time_to_last_solution"] = self._search_timer.elapsed()

        def _on_finish_callback(self, ret: SolveResult) -> None:
            """
            Callback called once search has finished.
            Determine result of search with clingo-dl using --minimize-variable.

            :param ret: Result of solve call.
            :type ret: SolveResult
            """
            if ret.satisfiable:
                self._stats["result"] = Result.SAT

            if (
                ret.exhausted 
                and ret.unsatisfiable
                and not self._is_interrupted 
                and not self._is_cutoff
            ):
                if self._last_solution is None:
                    self._stats["result"] = Result.UNSAT
                else:
                    self._stats["result"] = Result.OPTIMUM_FOUND

        def search(self, cut_off_time: float, require_solution: bool) -> tuple[Solution, dict[str, Any]]:
            """
            Search for new solution with clingo-dl using --minimize-variable.

            :param cut_off_time: Cut-off-time.
            :type cut_off_time: float
            :param require_solution: Whether any solution is required.
            :type require_solution: bool
            :return: Last solution and statistics.
            :rtype: tuple[Solution, dict[str, Any]]
            """
            super().search(cut_off_time, require_solution)

            while (
                not self._is_cutoff 
                and not self._is_interrupted 
                and not self._stats["result"] in [Result.UNSAT, Result.OPTIMUM_FOUND]
            ):
                self._add_bound_atom([self._last_solution.cost[0] - 1])
                with self._ctl.solve(
                    on_model=self._on_model_callback, 
                    on_statistics=self._on_statistics_callback,
                    on_finish=self._on_finish_callback,
                    async_=True
                ) as handle:
                    self._cut_off_timer.restart()
                    while not handle.wait(0):
                        self._cutoff(handle, cut_off_time, require_solution)

            if self._prev_bound_atom is not None:
                self._ctl.release_external(self._prev_bound_atom)
                self._prev_bound_atom = None

            self._bound_step += 1

            return self._last_solution, self._stats

if importlib.util.find_spec("clingcon"):
    class Clingcon(ClingoTheory):
        """
        clingcon.

        :param ctl: Control object for grounding/solving process.
        :type ctl: Control
        """
        def __init__(self, ctl: Control):
            super().__init__(ctl, ClingconTheory())
            self._objective = {"type": None, "vars": set()}

        def _read_asts(self, asts: list[AST]) -> None:
            """
            Read asts of input files and extract variables to minimize/maximize.

            :param asts: AST objects.
            :type asts: list[AST]
            """
            super()._read_asts(asts)
            for ast in asts:
                for item in ast.items():
                    if (
                        item[0] == 'head'
                        and item[1].ast_type == ASTType.TheoryAtom
                        and item[1].term.ast_type == ASTType.Function
                    ):
                        name = item[1].term.name
                        if name in ["minimize", "maximize"]:
                            if self._objective["type"] is None:
                                self._objective["type"] = name
                            elif self._objective["type"] != name:
                                continue
                            for elem in item[1].elements:
                                self._objective["vars"].add(str(elem))

        def read(self, files: list[str]) -> None:
            """
            Call parent method
            and add integer linear constraint to set bound for objective function.

            :param files: Input files.
            :type files: list[str]
            """
            super().read(files)
            if self._objective["vars"]:
                vars = ";".join(self._objective["vars"])
                if self._objective["type"] == "minimize":
                    operator = "<="
                else:
                    operator = ">="
                self._add_bound_subprogram(f"&sum {{{vars}}} {operator} B :- __b(B,t).")

        def add_bound(self, bound: list[int]) -> None:
            """
            Call parent method if clingo's minimize/maximize statements are used.
            Otherwise, add bound for objective function by adding atom of __b/2.

            :param bound: Bound for objective function.
            :type bound: list[int]
            """
            if not self._objective["vars"]:
                super().add_bound(bound)
            else:
                self._add_bound_atom(bound)
                self._bound_step += 1

        def _on_model_callback(self, model: Model) -> None:
            """
            Callback for intercepting models.
            Call parent method if clingo's minimize/maximize statements are used.
            Otherwise, extract first argument of atom of __csp_cost/1,
            update last solution, and restart timer to measure time since last solution.

            :param model: Model object.
            :type model: Model
            """
            if not self._objective["vars"]:
                super()._on_model_callback(model)
            else:
                self._thy.on_model(model)
                for atom in model.symbols(theory=True):
                    if atom.match("__csp_cost", 1):
                        self._last_solution = Solution(
                            model.symbols(shown=True),
                            model.symbols(atoms=True),
                            [int(atom.arguments[0].string)]
                        )
                        break
                logger.info("Optimization:", *self._last_solution.cost)
                self._cut_off_timer.restart()
                self._stats["time_to_last_solution"] = self._search_timer.elapsed()