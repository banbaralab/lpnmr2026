from clingo.application import ApplicationOptions, Flag
from clingo.control import Control
from clingo.symbol import parse_term, Symbol
import importlib.util
import inspect
import logging
import os
import re
from typing import Any
import uuid

DEFAULT_INIT_CUT_OFF_TIME = 10
DEFAULT_ITER_CUT_OFF_TIME = 5

DEFAULT_LEX_WEIGHT = 1000
DEFAULT_LEARNIGN_RATE = 0.5

DEFAULT_ITER_HEURISTIC = "Domain"

DEFAULT_NO_IMPROVEMENT_CUTOFF_THRESHOLD = 2
DEFAULT_CUT_OFF_TIME_INCREASE_PERCENT= 5

DEFAULT_SOLVER = "clingo"
DEFAULT_AUTO_RESOLVER = "simple"

DEFAULT_RANDOM_SEED = 0

ITER_OPT_MODE_DESCRIPTION = """Configure optimization algorithm for each iteration
      <arg>: <mode>[,<bound>]
        <mode> : {opt|enum|optN|ignore}
          opt   : Find optimal model
          enum  : Find models with costs <= initial bound
          optN  : Find optimum, then enumerate optimal models
          ignore: Ignore optimize statements
        <bound>: {<n>...,static|<n>[,dynamic][,<type {lt|leq}>]}
          <n>...,static     : Set initial bound for objective function(s) to <n>...
          <n>[,dynamic][,lt]: Set initial bound for objective function(s) to ((100 + <n>)%% of the current solution cost) - 1
          <n>[,dynamic],leq : Set initial bound for objective function(s) to ((100 + <n>)%% of the current solution cost)"""

class HeulingoOptions:
    """
    Manager for heulingo-specific options.
    """
    _has_iter_restart_on_model = False

    @classmethod
    def prepare(cls, args: list[str]) -> None:
        """
        Prepare HeulingoOptions object based on command-line arguments before running parsers.

        :param args: Command-line arguments.
        :type args: list[str]
        """
        for arg in args:
            if re.match(r"--(no-)?iter-r", arg):
                cls._has_iter_restart_on_model = True

    def __init__(self):
        self._group = "Heulingo Options"
        self._dummy_ctl = Control()
        self._debug = Flag()

        self._solver = DEFAULT_SOLVER
        self._solvers = ["clingo"]
        if importlib.util.find_spec("clingodl"):
            self._solvers.append("clingo-dl")
        if importlib.util.find_spec("clingcon"):
            self._solvers.append("clingcon")

        self._context = None

        self._auto_resolver = DEFAULT_AUTO_RESOLVER
        self._auto_resolvers = ["simple", "avg"]

        self._minimize_variable = None
        self._alnps_params = {
            "init_cut_off_time": DEFAULT_INIT_CUT_OFF_TIME,
            "iter_cut_off_time": DEFAULT_ITER_CUT_OFF_TIME,
            "iter_solver_config": {
                "restart_on_model": Flag(),
                "heuristic": DEFAULT_ITER_HEURISTIC,
            },
            "is_cost_bounded": False,
            "bound_params": {},
            "update_cutoff_params": {
                "no_improvement_cutoff_threshold": DEFAULT_NO_IMPROVEMENT_CUTOFF_THRESHOLD,
                "cut_off_time_increase_percent": DEFAULT_CUT_OFF_TIME_INCREASE_PERCENT
            }
        }
        self._strategy_params = {
                "lex_weight": DEFAULT_LEX_WEIGHT,
                "learning_rate": DEFAULT_LEARNIGN_RATE,
        }
        self._random_seed = DEFAULT_RANDOM_SEED

    @property
    def log_level(self) -> int:
        """
        Get log level based on debug flag.

        :return: DEBUG level if debug flag is set, otherwise INFO.
        :rtype: int
        """
        if self._debug:
            return logging.DEBUG
        else:
            return logging.INFO

    @property
    def solver(self) -> str:
        """
        Get selected solver.

        :return: Solver name.
        :rtype: str
        """
        return self._solver

    @property
    def context(self) -> Any:
        """
        Get context object.

        :return: Context object.
        :rtype: Any
        """
        return self._context

    @property
    def auto_resolver(self) -> str:
        """
        Get selected resolver for computing destruction percentages of auto-mode destroy operators.

        :return: Auto rolver name.
        :rtype: str
        """
        return self._auto_resolver

    @property
    def minimize_variable(self) -> Symbol | None:
        """
        Get variable for clingo-dl's option --minimize-variable.

        :return: Variable, or None if unset.
        :rtype: Symbol | None
        """
        return self._minimize_variable

    @property
    def alnps_params(self) -> dict[str, Any]:
        """
        Get parameters for ALNPS class.

        :return: Dictionary of parameters for ALNPS class.
        :rtype: dict[str, Any]
        """
        params = self._alnps_params.copy()
        if self.__class__._has_iter_restart_on_model:
            if params["iter_solver_config"]["restart_on_model"]:
                params["iter_solver_config"]["restart_on_model"] = "1"
            else:
                params["iter_solver_config"]["restart_on_model"] = "0"
        else:
            del params["iter_solver_config"]["restart_on_model"]
        return params

    @property
    def strategy_params(self) -> dict[str, Any]:
        """
        Get parameters for Strategy class.

        :return: Dictionary of parameters for Strategy class.
        :rtype: dict[str, Any]
        """
        return self._strategy_params

    @property
    def random_seed(self) -> int:
        """
        Get random seed.

        :return: Random seed.
        :rtype: int
        """
        return self._random_seed

    def _is_int(self, value: str) -> bool:
        try:
            int(value)
        except ValueError:
            return False
        return True

    def _is_positive_int(self, value: str) -> bool:
        if self._is_int(value):
            if int(value) <= 0:
                return False
        else:
            return False
        return True

    def _is_int_list(self, values: str) -> bool:
        for value in values:
            if not self._is_int(value):
                return False
        return True

    def _is_between_0_and_1(self, value: str) -> bool:
        try:
            float_value = float(value)
        except ValueError:
            return False
        if float_value < 0 or float_value > 1:
            return False
        return True

    def _is_term(self, value: str) -> bool:
        try:
            parse_term(value)
        except RuntimeError:
            return False
        return True

    def _solver_parser(self, value: str) -> bool:
        if value not in self._solvers:
            return False
        else:
            self._solver = value
        return True

    def _context_parser(self, value: str) -> bool:
        path = os.path.abspath(os.path.expanduser(value))
        if not os.path.isfile(path):
            return False

        spec = importlib.util.spec_from_file_location(f"context_{uuid.uuid4().hex}", path)
        if spec is None:
            return True

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        classes = [
            cls for _, cls in inspect.getmembers(module, inspect.isclass)
            if cls.__module__ == module.__name__
            and (cls.__init__ is object.__init__ or len(inspect.signature(cls.__init__).parameters) == 1)
        ]

        if classes:
            self._context = classes[0]()

        return True

    def _minimize_variable_parser(self, value: str) -> bool:
        if self._is_term(value):
            self._minimize_variable = parse_term(value)
            return True
        else:
            return False

    def _init_cut_off_time_parser(self, value: str) -> bool:
        if self._is_positive_int(value):
            self._alnps_params["init_cut_off_time"] = int(value)
            return True
        else:
            return False

    def _iter_cut_off_time_parser(self, value: str) -> bool:
        if self._is_positive_int(value):
            self._alnps_params["iter_cut_off_time"] = int(value)
            return True
        else:
            return False

    def _iter_configuration_parser(self, value: str) -> bool:
        try:
            self._dummy_ctl.configuration.configuration = value
        except RuntimeError:
            return False
        self._alnps_params["iter_solver_config"]["configuration"] = value
        return True

    def _iter_opt_strategy_parser(self, value: str) -> bool:
        try:
            self._dummy_ctl.configuration.solver.opt_strategy = value
        except RuntimeError:
            return False
        self._alnps_params["iter_solver_config"]["opt_strategy"] = value
        return True

    def _iter_opt_heuristic_parser(self, value: str) -> bool:
        try:
            self._dummy_ctl.configuration.solver.opt_heuristic = value
        except RuntimeError:
            return False
        self._alnps_params["iter_solver_config"]["opt_heuristic"] = value
        return True

    def _iter_heuristic_parser(self, value: str) -> bool:
        try:
            self._dummy_ctl.configuration.solver.heuristic = value
        except RuntimeError:
            return False
        self._alnps_params["iter_solver_config"]["heuristic"] = value
        return True

    def _iter_opt_mode_parser(self, value: str) -> bool:
        iter_opt_mode_parts = value.split(",")

        if iter_opt_mode_parts[0] not in ("opt", "enum", "optN", "ignore"):
            return False
        self._alnps_params["iter_solver_config"]["opt_mode"] = iter_opt_mode_parts[0]
        iter_opt_mode_parts = iter_opt_mode_parts[1:]

        if not iter_opt_mode_parts:
            self._alnps_params["is_cost_bounded"] = False
            return True
        else:
            self._alnps_params["is_cost_bounded"] = True

        if iter_opt_mode_parts[-1] in ("lt", "leq"):
            if iter_opt_mode_parts[-1] == "lt":
                self._alnps_params["bound_params"]["lt"] = True
            else:
                self._alnps_params["bound_params"]["lt"] = False
            iter_opt_mode_parts = iter_opt_mode_parts[:-1]
            if not iter_opt_mode_parts:
                return False
            if iter_opt_mode_parts[-1] == "dynamic":
                iter_opt_mode_parts = iter_opt_mode_parts[:-1]
            self._alnps_params["bound_params"]["dynamic"] = True
        else:
            if iter_opt_mode_parts[-1] in ("dynamic", "static"):
                if iter_opt_mode_parts[-1] == "dynamic":
                    self._alnps_params["bound_params"]["lt"] = True
                    self._alnps_params["bound_params"]["dynamic"] = True
                else:
                    self._alnps_params["bound_params"]["dynamic"] = False
                iter_opt_mode_parts = iter_opt_mode_parts[:-1]
                if not iter_opt_mode_parts:
                    return False
            else:
                self._alnps_params["bound_params"]["lt"] = True
                self._alnps_params["bound_params"]["dynamic"] = True

        if self._alnps_params["bound_params"]["dynamic"]:
            if len(iter_opt_mode_parts) != 1:
                return False
            if not self._is_int(iter_opt_mode_parts[0]):
                return False
            self._alnps_params["bound_params"]["percent"] = int(iter_opt_mode_parts[0])
        else:
            for cost in iter_opt_mode_parts:
                if not self._is_int(cost):
                    return False
            self._alnps_params["bound_params"]["bound"] = [int(cost) for cost in iter_opt_mode_parts]
        return True

    def _no_improvement_cutoff_threshold_parser(self, value: str) -> bool:
        if self._is_positive_int(value):
            self._alnps_params["update_cutoff_params"]["no_improvement_cutoff_threshold"] = int(value)
            return True
        else:
            return False

    def _cut_off_time_increase_percent_parser(self, value: str) -> bool:
        if self._is_positive_int(value):
            self._alnps_params["update_cutoff_params"]["cut_off_time_increase_percent"] = int(value)
            return True
        else:
            return False

    def _iter_lex_weight_parser(self, value: str) -> bool:
        if self._is_positive_int(value):
            self._strategy_params["lex_weight"] = int(value)
            return True
        else:
            return False

    def _iter_learning_rate_parser(self, value: str) -> bool:
        if self._is_between_0_and_1(value):
            self._strategy_params["learning_rate"] = float(value)
            return True
        else:
            return False

    def _auto_resolver_parser(self, value: str) -> bool:
        if value not in self._auto_resolvers:
            return False
        else:
            self._auto_resolver = value
        return True

    def _random_seed_parser(self, value: str) -> bool:
        if self._is_int(value):
            self._random_seed = int(value)
            return True
        else:
            return False

    def register_options(self, options: ApplicationOptions) -> None:
        """
        Register heulingo-specific options.

        :param options: ApplicationOptions object.
        :type options: ApplicationOptions
        """
        options.add_flag(
            self._group, 
            "debug",
            "Print debug information",
            self._debug
        )

        if importlib.util.find_spec("clingodl") or importlib.util.find_spec("clingcon"):
            options.add(
                self._group, 
                "solver",
                f"Use the ASP solver {{{'|'.join(self._solvers)}}} [{DEFAULT_SOLVER}]",
                self._solver_parser,
                argument="<arg>"
            )
            
        if importlib.util.find_spec("clingodl"):
            options.add(
                self._group, 
                "minimize-variable",
                f"Minimize the integer variable <arg> (for clingo-dl only)",
                self._minimize_variable_parser,
                argument="<arg>"
            )

        options.add(
            self._group,
            "context",
            f"Path to context file defining context class for @-syntax",
            self._context_parser,
            argument="<arg>"
        )

        options.add(
            self._group,
            "init-cut-off-time",
            f"Set cut-off-time for finding an initial solution to <n> seconds (<n> > 0) [{DEFAULT_INIT_CUT_OFF_TIME}]",
            self._init_cut_off_time_parser,
            argument="<n>"
        )

        options.add(
            self._group,
            "iter-cut-off-time",
            f"Set cut-off-time for iterations to <n> seconds (<n> > 0) [{DEFAULT_ITER_CUT_OFF_TIME}]",
            self._iter_cut_off_time_parser,
            argument="<n>"
        )

        options.add(
            self._group, 
            "iter-configuration",
            "Set default configuration for each iteration",
            self._iter_configuration_parser,
            argument="<arg>"
        )

        options.add(
            self._group, 
            "iter-opt-strategy",
            "Configure optimization strategy for each iteration",
            self._iter_opt_strategy_parser,
            argument="<arg>")

        options.add(
            self._group, 
            "iter-opt-heuristic",
            "Use opt for each iteration. in <list {{sign|model}}> heuristics",
            self._iter_opt_heuristic_parser,
            argument="<list>")

        options.add_flag(
            self._group, 
            "iter-restart-on-model",
            "Restart after each model for each iteration",
            self._alnps_params["iter_solver_config"]["restart_on_model"]
        )

        options.add(
            self._group, 
            "iter-heuristic,@2",
            f"Configure decision heuristic for each iteration [{DEFAULT_ITER_HEURISTIC}]",
            self._iter_heuristic_parser,
            argument="<heu>"
        )
        
        options.add(
            self._group, 
            "iter-opt-mode",
            ITER_OPT_MODE_DESCRIPTION,
            self._iter_opt_mode_parser,
            argument="<arg>")

        options.add(
            self._group,
            "no-improvement-cutoff-threshold",
            f"Increase cut-off-time if the number of consecutive iterations without improvement reaches <n> (<n> > 0) [{DEFAULT_NO_IMPROVEMENT_CUTOFF_THRESHOLD}]",
            self._no_improvement_cutoff_threshold_parser,
            argument="<n>"
        )

        options.add(
            self._group,
            "cut-off-time-increase-percent",
            f"Increase cut-off-time by <n>% (<n> > 0) [{DEFAULT_CUT_OFF_TIME_INCREASE_PERCENT}]",
            self._cut_off_time_increase_percent_parser,
            argument="<n>"
        )

        options.add(
            self._group,
            "lex-weight",
            f"Set weight factor for scalarizing lexicographic costs to <n> (<n> > 0) [{DEFAULT_LEX_WEIGHT}]",
            self._iter_lex_weight_parser,
            argument="<n>"
        )

        options.add(
            self._group,
            "learning-rate",
            f"Set learning rate for updating config weights to <f> (0 < <f> < 1) [{DEFAULT_LEARNIGN_RATE}]",
            self._iter_learning_rate_parser,
            argument="<f>"
        )

        options.add(
            self._group,
            "auto-resolver",
            f"Use the resolver for computing destruction percentages of auto-mode destroy operators. {{{'|'.join(self._auto_resolvers)}}} [{DEFAULT_AUTO_RESOLVER}]",
            self._auto_resolver_parser,
            argument="<arg>"
        )

        options.add(
            self._group,
            "random-seed",
            f"Set seed of Python’s random number generator to <n> [{DEFAULT_RANDOM_SEED}]",
            self._random_seed_parser,
            argument="<n>"
        )