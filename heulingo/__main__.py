from .alnps import ALNPS
from clingo.application import clingo_main, Application, ApplicationOptions
from clingo.control import Control
from importlib.metadata import version
import importlib.util
from .logger import HeulingoLogger
from .options import HeulingoOptions
import random
from .resolver import SimpleAutoResolver, AvgAutoResolver
import signal
from .solver import Clingo
from .strategy import RouletteWheelStrategy
import sys

if importlib.util.find_spec("clingodl"):
    from .solver import ClingoDL, ClingoDLMinimizeVariable
if importlib.util.find_spec("clingcon"):
    from .solver import Clingcon

class HeulingoApp(Application):
    """
    heulingo
    """
    def __init__(self):
        self.program_name = "heulingo"
        try:
            self.version = version("heulingo")
        except Exception:
            self.version = "1.0"
        self._options = HeulingoOptions()

    def register_options(self, options: ApplicationOptions) -> None:
        """
        Register heulingo's options.

        :param options: ApplicationOptions object.
        :type options: ApplicationOptions
        """
        self._options.register_options(options)

    def main(self, ctl: Control, files: list[str]) -> None:
        """
        Run main method of ALNPS class.

        :param ctl: Control object for grounding/solving process.
        :type ctl: Control
        :param files: Input files.
        :type files: list[str]
        """
        HeulingoLogger.set_level(self._options.log_level)

        if self._options.solver == "clingo":
            solver = Clingo(ctl)
        elif self._options.solver == "clingo-dl" and importlib.util.find_spec("clingodl"):
            if self._options.minimize_variable is None:
                solver = ClingoDL(ctl)
            else:
                solver = ClingoDLMinimizeVariable(ctl, self._options.minimize_variable)
        elif self._options.solver == "clingcon" and importlib.util.find_spec("clingcon"):
            solver = Clingcon(ctl)

        if self._options.auto_resolver == "simple":
            auto_resolver = SimpleAutoResolver()
        elif self._options.auto_resolver == "avg":
            auto_resolver = AvgAutoResolver()

        random.seed(self._options.random_seed)

        alnps = ALNPS(
            solver, 
            {
                "roulette": RouletteWheelStrategy(
                    self._options.strategy_params["learning_rate"],
                    self._options.strategy_params["lex_weight"],
                    auto_resolver
                )
            }
        )

        for signalnum in (signal.SIGINT, signal.SIGALRM, signal.SIGTERM):
            signal.signal(signalnum, alnps.handler)

        alnps.main(files, self._options.alnps_params, self._options.context)

def main():
    """
    Run heulingo main method.
    """
    args = sys.argv[1:]
    HeulingoOptions.prepare(args)
    clingo_main(HeulingoApp(), args)

if __name__ == "__main__":
    main()