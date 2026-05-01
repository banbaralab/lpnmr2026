from abc import ABC, abstractmethod
from clingo import Symbol
import copy
from .logger import logger
from .parser import ALNPSConfigParser
from typing import Any
from .solver import Solution

def calculate_actual_destruction_percent(destruction_candidate_atoms: set[Symbol], solution: Solution) -> float:
    """
    Return percentage of atoms subject to destruction actually destroyed in given solution.

    :param destruction_candidate_atoms: Atoms subject to destruction
    :type destruction_candidate_atoms: set[Symbol]
    :param solution: Solution used to determine destruction percentage.
    :type solution: Solution
    :return: Percentage of atoms subject to destruction that were destroyed.
    :rtype: float
    """
    if not destruction_candidate_atoms:
        return 0
    actual_destroyed_atoms = destruction_candidate_atoms - solution.shown
    actual_destruction_percent = (len(actual_destroyed_atoms) / len(destruction_candidate_atoms)) * 100
    return actual_destruction_percent

def is_new_solution_better(new_solution: Solution | None, current_solution: Solution) -> bool:
    """
    Check whether new solution is better than current solution.

    :param new_solution: New solution.
    :type new_solution: Solution | None
    :param current_solution: Current solution.
    :type current_solution: Solution
    :return: True if new solution is better than current solution, otherwise False.
    :rtype: bool
    """
    return new_solution is not None and new_solution.cost < current_solution.cost

class AutoResolver(ABC):
    """
    Resolver for computing destruction percentages of auto-mode destroy operators.
    """
    def resolve_config(self, lnps_config: dict[str, Any], stats: list[dict[str, Any]] = []) -> dict[str, Any]:
        """
        Resolve automatic values in LNPS configuration into concrete percentages.

        :param lnps_config: LNPS configuration containing automatic values.
        :type lnps_config: dict[str, Any]
        :param stats: Statistics. Defaults to [].
        :type stats: list[dict[str, Any]], optional
        :return: LNPS configuration with all automatic values replaced by concrete percentages.
        :rtype: dict[str, Any]
        """
        resolved_config = copy.deepcopy(lnps_config)
        for destroy_operator in resolved_config["destroy_operators"]:
            destroy_operator_name = destroy_operator["name"]
            for percent_or_number in destroy_operator["percents_or_numbers"]:
                if percent_or_number["type"] == "auto":
                    percent_or_number["type"] = "p"
                    destruction_percent = self._compute_auto_destruction_percent(lnps_config["name"], lnps_config["project_operators"], destroy_operator_name, stats)
                    logger.info(f"Auto destruction percent: {destruction_percent} (destroy operator: {destroy_operator_name})")
                    percent_or_number["value"] = destruction_percent
        return resolved_config

    @abstractmethod
    def _compute_auto_destruction_percent(self, config_name: str, project_operator_names: list[str], destroy_operator_name: str, stats: list[dict[str, Any]] = []) -> float:
        """
        Compute destruction percentage of auto-mode destroy operator.

        :param config_name: Config name.
        :type config_name: str
        :param project_operator_names: Project operator names.
        :type project_operator_names: list[str]
        :param destroy_operator_name: Destroy operator name.
        :type destroy_operator_name: str
        :param stats: Statistics. Defaults to [].
        :type stats: list[dict[str, Any]], optional
        :return: Destruction percentage of auto-mode destroy operator.
        :rtype: float
        """
        pass

class SimpleAutoResolver(AutoResolver):
    """
    Simplest algorithm for computing destruction percentages.

    :param auto_init_percent: Initial destruction percentage. Defaults to 0.
    :type auto_init_percent: int, optional
    """
    def __init__(self, auto_init_percent: int = 0):
        self._auto_init_percent = auto_init_percent
        self._last_improvement_stats  = None
        self._projected_atoms_cache = {}
        self._actual_destruction_percent_cache = {}

    def _update_last_improvement_stats(self, last_stats: dict[str, Any]) -> None:
        """
        Update statistics of last iteration where new solution was better than current solution.

        :param last_stats: Statistics of last iteration.
        :type last_stats: dict[str, Any]
        """
        if is_new_solution_better(last_stats["new_solution"], last_stats["current_solution"]):
            self._last_improvement_stats = last_stats
            self._projected_atoms_cache = {}
            self._actual_destruction_percent_cache = {}

    def resolve_config(self, lnps_config: dict[str, Any], stats: list[dict[str, Any]] = []) -> dict[str, Any]:
        """
        Resolve automatic values in LNPS configuration into concrete percentages
        based on last iteration’s statistics where new solution was better than current solution.

        :param lnps_config: LNPS configuration containing automatic values.
        :type lnps_config: dict[str, Any]
        :param stats: Statistics. Defaults to [].
        :type stats: list[dict[str, Any]], optional
        :return: LNPS configuration with all automatic values replaced by concrete percentages.
        :rtype: dict[str, Any]
        """
        if stats:
            self._update_last_improvement_stats(stats[-1])
        return super().resolve_config(lnps_config, stats)

    def _compute_auto_destruction_percent(self, config_name: str, project_operator_names: list[str], destroy_operator_name: str, stats: list[dict[str, Any]] = []) -> float:
        """
        Compute destruction percentage of auto-mode destroy operator based on actual destruction percentage.

        :param config_name: Config name.
        :type config_name: str
        :param project_operator_names: Project operator names.
        :type project_operator_names: list[str]
        :param destroy_operator_name: Destroy operator name.
        :type destroy_operator_name: str
        :param stats: Statistics. Defaults to [].
        :type stats: list[dict[str, Any]], optional
        :return: Destruction percentage of auto-mode destroy operator.
        :rtype: float
        """
        if self._last_improvement_stats is None:
            return self._auto_init_percent

        key = (config_name, destroy_operator_name)
        if key in self._actual_destruction_percent_cache:
            return self._actual_destruction_percent_cache[key]

        current_solution = self._last_improvement_stats["current_solution"]

        projected_atoms = set()
        for project_operator_name in project_operator_names:
            if project_operator_name not in self._projected_atoms_cache:
                self._projected_atoms_cache[project_operator_name] = ALNPSConfigParser.get_projected_atoms(current_solution, project_operator_name)
            projected_atoms.update(self._projected_atoms_cache[project_operator_name])

        destruction_candidate_atoms = ALNPSConfigParser.get_destruction_candidate_atoms(current_solution, projected_atoms, destroy_operator_name)
        actual_destruction_percent = calculate_actual_destruction_percent(destruction_candidate_atoms, self._last_improvement_stats["new_solution"])
        self._actual_destruction_percent_cache[key] = actual_destruction_percent
        return actual_destruction_percent

class AvgAutoResolver(AutoResolver):
    """
    Resolver using average of actual destruction percentages as destruction percentage.

    :param auto_init_percent: Initial destruction percentage. Defaults to 0.
    :type auto_init_percent: int, optional
    """
    def __init__(self, auto_init_percent: int = 0):
        self._auto_init_percent = auto_init_percent
        self._improvement_stats = []
        self._project_operator_names = {}
        self._actual_destruction_percents = {}

    def _compute_actual_destruction_percent(self, project_operator_names: list[str], destroy_operator_name: str, target_stats: dict[str, Any]) -> float:
        """
        Compute actual destruction percentage for given destroy operator with respect to projected atoms of current solution.

        :param project_operator_names: Project operator names.
        :type project_operator_names: list[str]
        :param destroy_operator_name: Destroy operator name.
        :type destroy_operator_name: str
        :param target_stats: Target statistics entry containing current and new solutions.
        :type target_stats: dict[str, Any]
        :return: Actual destruction percentage.
        :rtype: float
        """
        current_solution = target_stats["current_solution"]

        projected_atoms = set()
        for project_operator_name in project_operator_names:
            projected_atoms.update(ALNPSConfigParser.get_projected_atoms(current_solution, project_operator_name))

        destruction_candidate_atoms = ALNPSConfigParser.get_destruction_candidate_atoms(current_solution, projected_atoms, destroy_operator_name)
        actual_destruction_percent = calculate_actual_destruction_percent(destruction_candidate_atoms, target_stats["new_solution"])
        return actual_destruction_percent

    def _update_actual_destruction_percents(self, last_stats: dict[str, Any]) -> None:
        """
        Update stored actual destruction percentages using last improvement statistics.

        :param last_stats: Statistics of last iteration.
        :type last_stats: dict[str, Any]
        """
        self._improvement_stats.append(last_stats)
        for key in self._actual_destruction_percents.keys():
            self._actual_destruction_percents[key].append(self._compute_actual_destruction_percent(self._project_operator_names[key], key[1], last_stats))

    def _add_actual_destruction_percents_entry(self, key: tuple[str, str], project_operator_names: list[str]) -> None:
        """
        Add new entry for tracking actual destruction percentages.

        :param key: Tuple of config name and destroy operator name.
        :type key: tuple[str, str]
        :param project_operator_names: Project operator names.
        :type project_operator_names: list[str]
        """
        self._project_operator_names[key] = project_operator_names
        self._actual_destruction_percents[key] = []
        for target_stats in self._improvement_stats:
            self._actual_destruction_percents[key].append(self._compute_actual_destruction_percent(project_operator_names, key[1], target_stats))

    def resolve_config(self, lnps_config: dict[str, Any], stats: list[dict[str, Any]] = []) -> dict[str, Any]:
        """
        Resolve automatic values in LNPS configuration into concrete percentages
        based on observed statistics where new solution was better than current solution and
        counter of consecutive non-improving iterations for fallback handling.

        :param lnps_config: LNPS configuration containing automatic values.
        :type lnps_config: dict[str, Any]
        :param stats: Statistics. Defaults to [].
        :type stats: list[dict[str, Any]], optional
        :return: LNPS configuration with all automatic values replaced by concrete percentages.
        :rtype: dict[str, Any]
        """
        if stats:
            last_stats = stats[-1]
            if is_new_solution_better(last_stats["new_solution"], last_stats["current_solution"]):
                self._update_actual_destruction_percents(last_stats)
        return super().resolve_config(lnps_config, stats)

    def _compute_auto_destruction_percent(self, config_name: str, project_operator_names: list[str], destroy_operator_name: str, stats: list[dict[str, Any]] = []) -> float:
        """
        Compute destruction percentage of auto-mode destroy operator based on actual destruction percentages.

        :param config_name: Config name.
        :type config_name: str
        :param project_operator_names: Project operator names.
        :type project_operator_names: list[str]
        :param destroy_operator_name: Destroy operator name.
        :type destroy_operator_name: str
        :param stats: Statistics. Defaults to [].
        :type stats: list[dict[str, Any]], optional
        :return: Destruction percentage of auto-mode destroy operator.
        :rtype: float
        """
        key = (config_name, destroy_operator_name)
        if key not in self._actual_destruction_percents:
            self._add_actual_destruction_percents_entry(key, project_operator_names)

        if not self._actual_destruction_percents[key]:
            return self._auto_init_percent

        actual_destruction_percents = self._actual_destruction_percents[key]
        return sum(actual_destruction_percents) / len(actual_destruction_percents)