from clingo.symbol import Symbol, SymbolType, Tuple_
from .logger import logger
import logging
from .solver import Solution
from typing import Any

class ALNPSConfigParser:
    """
    Parser for extracting and validating ALNPS configuration from solution.
    """
    @staticmethod
    def _is_atom(term: Symbol) -> bool:
        """
        Check if given term is atom.

        :param term: Term.
        :type term: Symbol
        :return: True if given term is atom, False otherwise.
        :rtype: bool
        """
        return term.type == SymbolType.Function and term.name

    @classmethod
    def _get_project_operators_and_signatures_from_project2(cls, solution: Solution) -> tuple[set[str], list[dict[str, Any]]]:
        """
        Extract and validate project operator names and predicate signatures of projected atoms from atoms of _project/2 in solution.

        :param solution: Solution object.
        :type solution: Solution
        :return: Set of project operator names and list of predicate names and arities of projected atoms.
        :rtype: tuple[set[str], list[dict[str, Any]]]
        """
        project_operators = set()
        projected_signatures = []

        for atom in solution.true:
            if atom.match("_project", 2):
                project_operators.add(str(atom.arguments[0]))
                second_arg = atom.arguments[1]
                if cls._is_atom(second_arg):
                    projected_signature = {"name": second_arg.name, "arity": len(second_arg.arguments)}
                else:
                    logger.warning(f"_project/2: Second argument {second_arg} is not an atom. (atom: {atom})")
                    continue
                if projected_signature not in projected_signatures:
                    projected_signatures.append(projected_signature)

        return project_operators, projected_signatures

    @classmethod
    def _get_project_operators_and_signatures(cls, solution: Solution) -> tuple[set[str], list[dict[str, Any]]]:
        """
        Extract project operator names and predicate signatures of projected atoms from solution.

        :param solution: Solution object.
        :type solution: Solution
        :return: Set of project operator names and list of predicate names and arities of projected atoms.
        :rtype: tuple[set[str], list[dict[str, Any]]]
        """
        project_operators, projected_signatures = cls._get_project_operators_and_signatures_from_project2(solution)

        if not project_operators:
            project_operators.add("default")
            for atom in solution.shown:
                if cls._is_atom(atom):
                    projected_signature = {"name": atom.name, "arity": len(atom.arguments)}
                else:
                    continue
                if projected_signature not in projected_signatures:
                    projected_signatures.append(projected_signature)

        return project_operators, projected_signatures

    @staticmethod
    def _is_percent_or_number(term: Symbol) -> bool:
        """
        Check if given term is atom representing percent or number.

        :param term: Term.
        :type term: Symbol
        :return: True if given term is atom representing percent or number, False otherwise.
        :rtype: bool
        """
        return (term.match("p", 1) or term.match("n", 1)) and term.arguments[0].type == SymbolType.Number

    @classmethod
    def _get_destroy_operators_from_destroy2(cls, solution: Solution) -> dict[str, list[list[dict[str, Any]]]]:
        """
        Extract and validate destroy operators from atoms of _destroy/2 in solution.

        :param solution: Solution object.
        :type solution: Solution
        :return: Dictionary mapping destroy operator names to lists of percentages or numbers.
        :rtype: dict[str, list[list[dict[str, Any]]]]
        """
        destroy_operators = {}

        for atom in solution.true:
            if atom.match("_destroy", 2):
                name = str(atom.arguments[0])
                if name not in destroy_operators:
                    destroy_operators[name] = []

                second_arg = atom.arguments[1]
                if second_arg.type != SymbolType.Function:
                    logger.warning(f"_destroy/2: Second argument {second_arg} is invalid. (atom: {atom})")
                    continue
                percents_or_numbers = []
                if second_arg.name:
                    if second_arg.match("auto", 0):
                        percents_or_numbers.append({"type":  second_arg.name, "value": None})
                    elif cls._is_percent_or_number(second_arg):
                        percents_or_numbers.append({"type":  second_arg.name, "value": second_arg.arguments[0].number})
                    else:
                        logger.warning(f"_destroy/2: Second argument {second_arg} is invalid. (atom: {atom})")
                        continue
                else:
                    for arg in second_arg.arguments:
                        if cls._is_percent_or_number(arg):
                            percents_or_numbers.append({"type": arg.name, "value": arg.arguments[0].number})
                        else:
                            logger.warning(f"_destroy/2: Second argument {second_arg} is invalid. (atom: {atom})")
                            break
                    if len(percents_or_numbers) < len(second_arg.arguments):
                        continue
                destroy_operators[name].append(percents_or_numbers)

        for name in destroy_operators.keys():
            if not destroy_operators[name]:
                destroy_operators[name].append([{"type": "auto", "value": None}])

        return destroy_operators

    @classmethod
    def _get_destroy_operators_from_destroy3(cls, solution: Solution) -> dict[str, list[list[dict[str, Any]]]]:
        """
        Extract and validate destroy operators from atoms of _destroy/3 in solution.

        :param solution: Solution object.
        :type solution: Solution
        :return: Dictionary mapping destroy operator names to default percentage.
        :rtype: dict[str, list[list[dict[str, Any]]]]
        """
        destroy_operators = {}

        for atom in solution.true:
            if atom.match("_destroy", 3):
                name = str(atom.arguments[0])
                if name not in destroy_operators:
                    destroy_operators[name] = [[{"type": "auto", "value": None}]]

                second_arg = atom.arguments[1]
                if not cls._is_atom(second_arg):
                    logger.warning(f"_destroy/3: Second argument {second_arg} is not an atom. (atom: {atom})")

        return destroy_operators

    @classmethod
    def _get_destroy_operators(cls, solution: Solution) -> dict[str, list[list[dict[str, Any]]]]:
        """
        Combine destroy operators extracted from atoms of _destroy/2 and _destroy/3.

        :param solution: Solution object.
        :type solution: Solution
        :return: Dictionary mapping destroy operator names to lists of percentages or numbers.
        :rtype: dict[str, list[list[dict[str, Any]]]]
        """
        destroy_operators = {
            **cls._get_destroy_operators_from_destroy3(solution),
            **cls._get_destroy_operators_from_destroy2(solution)
        }

        if not destroy_operators:
            destroy_operators["default"] = [[{"type": "auto", "value": None}]]

        return destroy_operators

    @staticmethod
    def _is_heuristic_modifier(term: Symbol) -> bool:
        """
        Check if given term is modifier used in #heuristic statements.

        :param term: Term.
        :type term: Symbol
        :return: True if given term is heuristic modifier, False otherwise.
        :rtype: bool
        """
        return term.match("sign", 0) or term.match("level", 0) or term.match("true", 0) or term.match("false", 0) or term.match("init", 0) or term.match("factor", 0)

    @classmethod
    def _get_prioritize_operators_from_prioritize3(cls, solution: Solution) -> dict[str, list[dict[str, Any]]]:
        """
        Extract and validate prioritize operators from atoms of _prioritize/3 in solution.

        :param solution: Solution object.
        :type solution: Solution
        :return: Dictionary mapping prioritize operator names to lists of heuristic modifiers and their values.
        :rtype: dict[str, list[dict[str, Any]]]
        """
        prioritize_operators = {}

        for atom in solution.true:
            if atom.match("_prioritize", 3):
                name = str(atom.arguments[0])
                if name not in prioritize_operators:
                    prioritize_operators[name] = []

                second_arg = atom.arguments[1]
                if second_arg.match("inf", 0):
                    value = "inf"
                elif second_arg.type == SymbolType.Number:
                    value = second_arg.number
                else:
                    logger.warning(f"_prioritize/3: Second argument {second_arg} is neither an integer nor inf. (atom: {atom})")
                    continue

                third_arg = atom.arguments[2]
                if cls._is_heuristic_modifier(third_arg):
                    prioritize_operators[name].append({"value": value, "modifier": third_arg.name})
                else:
                    logger.warning(f"_prioritize/3: Third argument {third_arg} is not one of: sign, level, true, false, init, factor. (atom: {atom})")

        for name in prioritize_operators.keys():
            if not prioritize_operators[name]:
                prioritize_operators[name].append({"value": 1, "modifier": "true"})

        return prioritize_operators

    @classmethod
    def _get_prioritize_operators_from_prioritize2(cls, solution: Solution) -> dict[str, list[dict[str, Any]]]:
        """
        Extract and validate prioritize operators from atoms of _prioritize/2 in solution.

        :param solution: Solution object.
        :type solution: Solution
        :return: Dictionary mapping prioritize operator names to default heuristic modifier and its value.
        :rtype: dict[str, list[dict[str, Any]]]
        """
        prioritize_operators = {}

        for atom in solution.true:
            if atom.match("_prioritize", 2):
                name = str(atom.arguments[0])
                if name not in prioritize_operators:
                    prioritize_operators[name] = [{"value": 1, "modifier": "true"}]

                second_arg = atom.arguments[1]
                if not cls._is_atom(second_arg):
                    logger.warning(f"_prioritize/2: Second argument {second_arg} is not an atom. (atom: {atom})")

        return prioritize_operators

    @classmethod
    def _get_prioritize_operators(cls, solution: Solution) -> dict[str, list[dict[str, Any]]]:
        """
        Combine prioritize operators extracted from atoms of _prioritize/2 and _prioritize/3.

        :param solution: Solution object.
        :type solution: Solution
        :return: Dictionary mapping prioritize operator names to lists of heuristic modifiers and their values.
        :rtype: dict[str, list[dict[str, Any]]]
        """
        prioritize_operators = {
            **cls._get_prioritize_operators_from_prioritize2(solution),
            **cls._get_prioritize_operators_from_prioritize3(solution)
        }

        if not prioritize_operators:
            prioritize_operators["default"] = [{"value": 1, "modifier": "true"}]

        return prioritize_operators

    @classmethod
    def _get_configs(cls, solution: Solution, defined_project_operators: list[str], defined_destroy_operators: list[str], defined_prioritize_operators: list[str]) -> dict[str, dict[str, list[str]]]:
        """
        Extract and validate configurations from atoms of _config/4.

        :param solution: Solution object.
        :type solution: Solution
        :param defined_project_operators: List of available project operator names.
        :type defined_project_operators: list[str]
        :param defined_destroy_operators: List of available destroy operator names.
        :type defined_destroy_operators: list[str]
        :param defined_prioritize_operators: List of available prioritize operator names.
        :type defined_prioritize_operators: list[str]
        :return: Dictionary mapping configuration names to lists of operator names.
        :rtype: dict[str, dict[str, list[str]]]
        """
        configs = {}
        defined_operators = {
            "project_operators": defined_project_operators,
            "destroy_operators": defined_destroy_operators,
            "prioritize_operators": defined_prioritize_operators
        }
        operator_args_info = [
            {"index": 1, "key": "project_operators", "ordinal": "Second", "type": "Project"},
            {"index": 2, "key": "destroy_operators", "ordinal": "Third",  "type": "Destroy"},
            {"index": 3, "key": "prioritize_operators", "ordinal": "Fourth", "type": "Prioritize"},
        ]

        for atom in solution.true:
            if atom.match("_config", 4):
                config_name = str(atom.arguments[0])
                if config_name not in configs:
                    configs[config_name] = {"project_operators": [], "destroy_operators": [], "prioritize_operators": []}

                for info in operator_args_info:
                    key = info["key"]
                    operator_name = str(atom.arguments[info["index"]])
                    if operator_name in defined_operators[key]:
                        if operator_name not in configs[config_name][key]:
                            configs[config_name][key].append(operator_name)
                    else:
                        logger.warning(f"_config/4: {info['type']} operator {operator_name} is not defined. (atom: {atom})")

        if not configs:
            configs["default"] = {
                "project_operators": defined_project_operators,
                "destroy_operators": defined_destroy_operators, 
                "prioritize_operators": defined_prioritize_operators
            }

        sorted_configs = {
            config_name: {
                key: sorted(operator_names)
                for key, operator_names in operators.items()
            }
            for config_name, operators in configs.items()
        }

        return sorted_configs

    @classmethod
    def _read_strategy(cls, solution: Solution, defined_configs: dict[str, dict[str, list[str]]], defined_strategies: list[str], default_strategy: str) -> tuple[str, dict[str, dict[str, list[str]]]]:
        """
        Extract and validate strategy and configurations subject to selection from atoms of _strategy/2.

        :param solution: Solution object.
        :type solution: Solution
        :param defined_configs: Dictionary mapping names of available configurations to lists of operator names.
        :type defined_configs: dict[str, dict[str, list[str]]]
        :param defined_strategies: List of available strategy names.
        :type defined_strategies: list[str]
        :param default_strategy: Name of strategy to use when not specified.
        :type default_strategy: str
        :return: Strategy name and Dictionary mapping names of configurations subject to selection to lists of operator names.
        :rtype: tuple[str, dict[str, dict[str, list[str]]]]
        """
        strategy = None
        candidate_configs = {}

        for atom in solution.true:
            if atom.match("_strategy", 2):
                strategy_name = str(atom.arguments[0])
                if strategy_name not in defined_strategies:
                    logger.warning(f"_strategy/2: Strategy {strategy_name} is not defined. (atom: {atom})")
                    continue

                if strategy is None:
                    strategy = strategy_name
                if strategy != strategy_name:
                    logger.warning(f"_strategy/2: Multiple strategies specified. Using {strategy} and ignoring {strategy_name}. (atom: {atom})")
                    continue

                config_name = str(atom.arguments[1])
                if config_name in defined_configs:
                    candidate_configs[config_name] = defined_configs[config_name]
                else:
                    logger.warning(f"_strategy/2: Config {config_name} is not defined. (atom: {atom})")

        if not candidate_configs:
            candidate_configs = defined_configs.copy()
        if strategy is None:
            strategy = default_strategy

        return strategy, candidate_configs

    @classmethod
    def get_alnps_config(cls, solution: Solution, defined_strategies: list[str], default_strategy: str) -> dict[str, Any]:
        """
        Extract and validate ALNPS configuration from solution.

        ALNPS configuration includes project operator names, predicate signatures of projected atoms,
        destroy operator definitions, prioritize operator definitions,
        configuration definitions and strategy name.

        :param solution: Solution object.
        :type solution: Solution
        :param defined_strategies: List of available strategy names.
        :type defined_strategies: list[str]
        :param default_strategy: Name of strategy to use when not specified.
        :type default_strategy: str
        :return: ALNPS configuration dictionary with the following keys:
            - "project_operators" (set[str]): Set of project operator names.
            - "projected_signatures" (list[dict[str, Any]]): List of dictionaries with the following keys:
                - "name" (str): Predicate name of projected atom.
                - "arity" (int): Arity of projected atom.
            - "destroy_operators" (dict[str, list[list[dict[str, Any]]]]): Dictionary mapping destroy operator names to nested lists of dictionaries with the following keys:a
                - "type" (str): Type of percentage or number ("p", "n", or "auto").
                - "value" (int | None): Value of percentage or number.
            - "prioritize_operators" (dict[str, list[dict[str, Any]]]): Dictionary mapping prioritize operator names to lists of dictionaries with the following keys:
                - "value" (int | str): Value of heuristic modifier (integer or "inf").
                - "modifier" (str): Heuristic modifier ("sign", "level", "true", "false", "init", or "factor").
            - "configs" (dict[str, dict[str, list[str]]]): Dictionary mapping configuration names to dictionaries with the following keys:
                - "project_operators" (list[str]): List of project operator names.
                - "destroy_operators" (list[str]): List of destroy operator names.
                - "prioritize_operators" (list[str]): List of prioritize operator names.
            - "strategy" (str): Strategy name
        :rtype: dict[str, Any]
        """
        project_operators, projected_signatures = cls._get_project_operators_and_signatures(solution)
        destroy_operators = cls._get_destroy_operators(solution)
        prioritize_operators = cls._get_prioritize_operators(solution)
        defined_configs = cls._get_configs(solution, list(project_operators), list(destroy_operators.keys()), list(prioritize_operators.keys()))
        strategy, candidate_configs = cls._read_strategy(solution, defined_configs, defined_strategies, default_strategy)
        alnps_config = {
            "project_operators": project_operators,
            "projected_signatures": projected_signatures,
            "destroy_operators": destroy_operators,
            "prioritize_operators": prioritize_operators,
            "configs": candidate_configs,
            "strategy": strategy
        }
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("ALNPS configuration:", cls._format_alnps_config(alnps_config))
        return alnps_config

    @classmethod
    def _format_alnps_config(cls, alnps_config: dict[str, Any]) -> str:
        """
        Convert ALNPS configuration into string.

        :param alnps_config: ALNPS configuration.
        :type alnps_config: dict[str, Any]
        :return: String representing ALNPS configuration.
        :rtype: str
        """
        project_operators = ",".join(alnps_config["project_operators"])

        projected_signatures = ",".join(
            f"{signature['name']}/{signature['arity']}"
            for signature in alnps_config["projected_signatures"]
        )

        destroy_operators = ",".join(
            name + "{" + ",".join(
                "[" + ",".join(
                    f"{pn['type']}({pn['value']})" if pn['value'] is not None else pn['type']
                    for pn in percents_or_numbers
                )+ "]"
                for percents_or_numbers in percents_or_numbers_list
            )+ "}"
            for name, percents_or_numbers_list in alnps_config["destroy_operators"].items()
        )
        prioritize_operators = ",".join(
            name + "{"+ ",".join(
                f"[{mv['value']},{mv['modifier']}]"
                for mv in modifiers_and_values
            ) + "}"
            for name, modifiers_and_values in alnps_config["prioritize_operators"].items()
        )

        configs = ",".join(
            config + "[" + "project_operators={"+ ",".join(
                operators["project_operators"]
            )+ "},destroy_operators={" + ",".join(
                operators["destroy_operators"]
            )+ "},prioritize_operators={" + ",".join(
                operators["prioritize_operators"]
            )+ "}" + "]"
            for config, operators in alnps_config["configs"].items()
        )

        strategy = alnps_config["strategy"]

        return f"project_operators={{{project_operators}}}, projected_signatures={{{projected_signatures}}}, destroy_operators={{{destroy_operators}}}, prioritize_operators={{{prioritize_operators}}}, configs={{{configs}}}, strategy={strategy}"

    @classmethod
    def get_projected_atoms(cls, solution: Solution, project_operator_name: str) -> set[Symbol]:
        """
        Extract subset of atoms included in answer set from atoms of _project/2.

        :param solution: Current solution.
        :type solution: Solution
        :param project_operator_name: Project operator name.
        :type project_operator_name: str
        :return: Projected atoms.
        :rtype: set[Symbol]
        """
        projected_atoms = set()
        is_project2_defined = False
        for atom in solution.true:
            if atom.match("_project", 2):
                operator_name = str(atom.arguments[0])
                if operator_name == project_operator_name:
                    is_project2_defined = True
                    second_arg = atom.arguments[1]
                    if cls._is_atom(second_arg) and second_arg in solution.shown:
                        projected_atoms.add(second_arg)

        if not is_project2_defined:
            for atom in solution.shown:
                if cls._is_atom(atom):
                    projected_atoms.add(atom)

        return projected_atoms

    @classmethod
    def get_atom_term_pairs(cls, solution: Solution, projected_atoms: set[Symbol], destroy_operator_name: str) -> list[dict[str, Symbol]]:
        """
        Extract atoms subject to destruction and corresponding terms from atoms of _destroy/3.

        :param solution: Current solution.
        :type solution: Solution
        :param projected_atoms: Projected atoms.
        :type projected_atoms: set[Symbol]
        :param destroy_operator_name: Destroy operator name.
        :type destroy_operator_name: str
        :return: Atoms subject to destruction and corresponding terms.
        :rtype: list[dict[str, Symbol]]
        """
        atom_term_pairs = []
        is_destroy3_defined = False

        for atom in solution.true:
            if atom.match("_destroy", 3):
                operator_name = str(atom.arguments[0])
                if operator_name == destroy_operator_name:
                    is_destroy3_defined = True
                    candidate_atom = atom.arguments[1]
                    if candidate_atom in projected_atoms:
                        atom_term_pairs.append({"atom": candidate_atom, "term": atom.arguments[2]})

        if not is_destroy3_defined:
            for atom in projected_atoms:
                atom_term_pairs.append({"atom": atom, "term": Tuple_(atom.arguments)})

        return atom_term_pairs

    @classmethod
    def get_destruction_candidate_atoms(cls, solution: Solution, projected_atoms: set[Symbol], destroy_operator_name: str) -> set[Symbol]:
        """
        Extract atoms subject to destruction from atoms of _destroy/3.

        :param solution: Current solution.
        :type solution: Solution
        :param projected_atoms: Projected atoms.
        :type projected_atoms: set[Symbol]
        :param destroy_operator_name: Destroy operator name.
        :type destroy_operator_name: str
        :return: Atoms subject to destruction.
        :rtype: set[Symbol]
        """
        atom_term_pairs = cls.get_atom_term_pairs(solution, projected_atoms, destroy_operator_name)
        return set(pair["atom"] for pair in atom_term_pairs)

    @classmethod
    def get_heuristic_targets(cls, solution: Solution, undestroyed_atoms: set[Symbol], prioritize_operator_name: str) -> set[Symbol]:
        """
        Extract atoms subject to prioritization from atoms of _prioritize/2.

        :param solution: Current solution.
        :type solution: Solution
        :param undestroyed_atoms: Undestroyed atoms.
        :type undestroyed_atoms: set[Symbol]
        :param prioritize_operator_name: Prioritize operator name.
        :type prioritize_operator_name: str
        :return: Atoms subject to prioritization.
        :rtype: set[Symbol]
        """
        heuristic_targets = set()
        is_prioritize2_defined = False

        for atom in solution.true:
            if atom.match("_prioritize", 2):
                operator_name = str(atom.arguments[0])
                if operator_name == prioritize_operator_name:
                    is_prioritize2_defined = True
                    candidate_atom = atom.arguments[1]
                    if candidate_atom in undestroyed_atoms:
                        heuristic_targets.add(candidate_atom)

        if not is_prioritize2_defined:
            heuristic_targets = undestroyed_atoms.copy()

        return heuristic_targets