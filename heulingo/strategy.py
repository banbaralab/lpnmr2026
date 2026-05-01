from abc import ABC, abstractmethod
import itertools
from .logger import logger
import logging
import random
from .resolver import AutoResolver
from .solver import Solution
from typing import Any

class Strategy(ABC):
    """
    Strategy to select LNPS configuration from ALNPS configuration.
    """
    @abstractmethod
    def get_initial_config(self, alnps_config: dict[str, Any], initial_solution: Solution) -> dict[str, Any]:
        """
        Abstract method to get initial LNPS configuration.

        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :param initial_solution: Initial solution.
        :type initial_solution: Solution
        :return: LNPS configuration dictionary with the following keys:
            - "name" (str): Name of LNPS configuration.
            - "project_operators" (list[str]): List of project operator names.
            - "destroy_operators" (list[dict[str, Any]]): List of dictionaries with the following keys:
                - "name" (str): Name of destroy operator.
                - "percents_or_numbers" (list[dict[str, Any]]): List of dictionaries with the following keys:
                    - "type" (str): Type of percentage or number ("p" or "n").
                    - "value" (int | float): Value of percentage or number.
            - "prioritize_operators" (list[dict[str, Any]]): List of dictionaries with the following keys:
                - "name" (str): Name of prioritize operator.
                - "value" (int | str): Value of heuristic modifier (integer or "inf").
                - "modifier" (str): Heuristic modifier ("sign", "level", "true", "false", "init", or "factor").
            - "key" (tuple[Any, ...]): Key of LNPS configuration.
        :rtype: dict[str, Any]
        """
        pass

    @abstractmethod
    def update_config(self, lnps_config: dict[str, Any], alnps_config: dict[str, Any], stats: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Abstract method to update LNPS configuration.

        :param lnps_config: Current LNPS configuration.
        :type lnps_config: dict[str, Any]
        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :param stats: Statistics.
        :type stats: list[dict[str, Any]]
        :return: New LNPS configuration.
        :rtype: dict[str, Any]
        """
        pass

class RouletteWheelStrategy(Strategy):
    """
    Roulette-wheel strategy.

    :param learning_rate: Learning rate used to update weights.
    :type learning_rate: float
    :param lex_weight: Weight used to convert lexicographic cost into integer cost.
    :type lex_weight: int
    :param resolver: Resolver for computing destruction percentages of auto-mode destroy operators.
    :type resolver: AutoResolver
    :param min_weight: Minimum value of weight. Defaults to 0.001.
    :type min_weight: float, optional
    """
    def __init__(self, learning_rate: float, lex_weight: int, resolver: AutoResolver, min_weight: float = 0.001):
        self._learning_rate = learning_rate
        self._lex_weight = lex_weight
        self._resolver = resolver
        self._min_weight = min_weight
        self._weights = {}

    def _compute_lex_weighted_sum(self, lex_costs: list[int]) -> int:
        """
        Convert lexicographic cost into integer cost by computing weighted sum.

        :param lex_costs: Lexicographic cost.
        :type lex_costs: list[int]
        :return: Integer cost.
        :rtype: int
        """
        num_lex_costs = len(lex_costs)
        last_lex_cost_idx =  num_lex_costs - 1
        cost = 0
        for i in range(num_lex_costs):
            cost += lex_costs[i]*(self._lex_weight**(last_lex_cost_idx-i))
        return cost

    def _generate_keys(self, alnps_config: dict[str, Any]) -> list[tuple[Any, ...]]:
        """
        Generate key corresponding to each LNPS configuration.

        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :return: Keys of LNPS configurations.
        :rtype: list[tuple[Any, ...]]
        """
        config_keys = []
        for config_name, operators in alnps_config["configs"].items():
            destroy_operator_names = operators["destroy_operators"]
            percents_or_numbers_indices = [
                [i for i in range(len(alnps_config["destroy_operators"][name]))] 
                for name in destroy_operator_names
            ]
            prioritize_operator_names = operators["prioritize_operators"]
            heuristic_modifiers_indices = [
                [i for i in range(len(alnps_config["prioritize_operators"][name]))] 
                for name in prioritize_operator_names
            ]

            operator_names = destroy_operator_names + prioritize_operator_names
            params_indices = percents_or_numbers_indices + heuristic_modifiers_indices
            for combination in itertools.product(*params_indices):
                config_key = [config_name]
                for operator, params_index in zip(operator_names, combination):
                    config_key.append(operator)
                    config_key.append(params_index)
                config_keys.append(config_key)
        return config_keys

    def _initialize_weights(self, alnps_config: dict[str, Any], initial_solution: Solution) -> None:
        """
        Initialize weights for all possible LNPS configurations using initial solution's cost.

        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :param initial_solution: Initial solution.
        :type initial_solution: Solution
        """
        if len(initial_solution.cost) > 1:
            initial_weight = abs(self._compute_lex_weighted_sum(initial_solution.cost))
        else:
            initial_weight = abs(initial_solution.cost[0])

        config_keys = self._generate_keys(alnps_config)
        for config_key in config_keys:
            self._weights[tuple(config_key)] = initial_weight

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Initial weight:", initial_weight)

    def _key_to_config(self, key: tuple[Any, ...], alnps_config: dict[str, Any]) -> dict[str, Any]:
        """
        Convert key into corresponding LNPS configuration.

        :param key: Key of LNPS configuration.
        :type key: tuple[Any, ...]
        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :return: LNPS configuration corresponding to key.
        :rtype: dict[str, Any]
        """
        config_name = key[0]
        config = {
            "name": config_name,
            "project_operators": alnps_config["configs"][config_name]["project_operators"],
            "destroy_operators": [],
            "prioritize_operators": [],
            "key": key
        }
        destroy_operator_count = len(alnps_config["configs"][config_name]["destroy_operators"])

        for i in range(1,len(key),2):
            operator_name = key[i]

            if i <= 2*destroy_operator_count:
                destroy_operator = {
                    "name": operator_name,
                    "percents_or_numbers": alnps_config["destroy_operators"][operator_name][key[i+1]]
                }
                config["destroy_operators"].append(destroy_operator)
            else:
                heuristic_modifier = alnps_config["prioritize_operators"][operator_name][key[i+1]]
                config["prioritize_operators"].append(
                    {
                        "name": operator_name,
                        "value": heuristic_modifier["value"],
                        "modifier": heuristic_modifier["modifier"]
                    }
                )

        config["config_repr"] = self._format_lnps_config(config)

        return config

    def _select_config(self, alnps_config: dict[str, Any]) -> dict[str, Any]:
        """
        Select LNPS configuration using roulette wheel selection based on normalized weights.

        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :return: Selected LNPS configuration.
        :rtype: dict[str, Any]
        """
        weights = self._weights.values()
        normalized_weights = [w / max(weights) for w in weights]
        config_key = random.choices(
            list(self._weights.keys()), 
            weights=normalized_weights, 
            k=1
        )[0]
        lnps_config = self._key_to_config(config_key, alnps_config)
        logger.info("Selected LNPS configuration:", lnps_config["config_repr"])
        return lnps_config

    def get_initial_config(self, alnps_config: dict[str, Any], initial_solution: Solution) -> dict[str, Any]:
        """
        Get initial LNPS configuration using roulette wheel selection after initializing weights.

        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :param initial_solution: Initial solution.
        :type initial_solution: Solution
        :return: LNPS configuration dictionary with the following keys:
            - "name" (str): Name of LNPS configuration.
            - "project_operators" (list[str]): List of project operator names.
            - "destroy_operators" (list[dict[str, Any]]): List of names and percentages or numbers of destroy operators.
            - "prioritize_operators" (list[dict[str, Any]]): List of names, heuristic modifiers, and their values of prioritize operators.
            - "key" (tuple[Any, ...]): Key of LNPS configuration.
            - "config_repr" (str): String representation of LNPS configuration.
        :rtype: dict[str, Any]
        """
        self._initialize_weights(alnps_config, initial_solution)
        return self._resolver.resolve_config(self._select_config(alnps_config))

    def _compute_effectiveness_score(self, current_soluion: Solution, new_solution: Solution | None, time_to_last_solution: float) -> float:
        """
        Compute effectiveness score of current LNPS configuration.

        :param current_soluion: Current solution.
        :type current_soluion: Solution
        :param new_solution: New solution found by using current LNPS configuration.
        :type new_solution: Solution | None
        :param time_to_last_solution: Elapsed time to new solution found.
        :type time_to_last_solution: float
        :return: Effectiveness score.
        :rtype: float
        """

        if new_solution is not None:
            if len(current_soluion.cost) > 1:
                current_soluion_cost = self._compute_lex_weighted_sum(current_soluion.cost)
                new_solution_cost = self._compute_lex_weighted_sum(new_solution.cost)
            else:
                current_soluion_cost = current_soluion.cost[0]
                new_solution_cost = new_solution.cost[0]
            return (current_soluion_cost - new_solution_cost) / time_to_last_solution
        else:
            return 0

    def _update_weights(self, config_key: tuple[Any, ...], effectiveness_score: float) -> None:
        """
        Update weight of LNPS configuration based on effectiveness score.

        :param config_key: Key of LNPS configuration.
        :type config_key: tuple[Any, ...]
        :param effectiveness_score: Effectiveness score.
        :type effectiveness_score: float
        """
        weight = self._weights[config_key]
        new_weight = (1 - self._learning_rate) * weight + self._learning_rate * effectiveness_score
        if new_weight < self._min_weight:
            new_weight = self._min_weight
        self._weights[config_key] = new_weight

    def update_config(self, lnps_config: dict[str, Any], alnps_config: dict[str, Any], stats: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Update weight of current LNPS configuration and select new LNPS configuration using roulette wheel selection.

        :param lnps_config: Current LNPS configuration.
        :type lnps_config: dict[str, Any]
        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :param stats: Statistics.
        :type stats: list[dict[str, Any]]
        :return: New LNPS configuration.
        :rtype: dict[str, Any]
        """
        effectiveness_score = self._compute_effectiveness_score(stats[-1]["current_solution"], stats[-1]["new_solution"], stats[-1]["time_to_last_solution"])

        config_key = lnps_config["key"]
        weight = self._weights[config_key]
        self._update_weights(config_key, effectiveness_score)
        new_weight = self._weights[config_key]
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(lnps_config["config_repr"], "weight:", weight, "->", new_weight)
        return self._resolver.resolve_config(self._select_config(alnps_config), stats)
    
    def _format_lnps_config(self, lnps_config: dict[str, Any]) -> str:
        """
        Convert LNPS configuration into string.

        :param lnps_config: LNPS configuration.
        :type lnps_config: dict[str, Any]
        :return: String representing LNPS configuration.
        :rtype: str
        """
        project_operators = ",".join(lnps_config["project_operators"])

        destroy_operators = ",".join(
            destroy_operator["name"] + "[" + ",".join(
                f"{percent_or_number['type']}({percent_or_number['value']})" if percent_or_number['value'] is not None else percent_or_number['type']
                for percent_or_number in destroy_operator["percents_or_numbers"]
            ) + "]"
            for destroy_operator in lnps_config["destroy_operators"]
        )
        
        prioritize_operators = ",".join(
            f"{prioritize_operator['name']}[{prioritize_operator['value']},{prioritize_operator['modifier']}]"
            for prioritize_operator in lnps_config["prioritize_operators"]
        )
        
        return f"{lnps_config['name']}[project_operators={{{project_operators}}},destroy_operators={{{destroy_operators}}},prioritize_operators={{{prioritize_operators}}}]"