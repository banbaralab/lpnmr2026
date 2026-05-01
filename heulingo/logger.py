import logging
from .timer import Timer
import sys

class HeulingoLogger:
    """
    Logger for heulingo.
    """
    _logger = None
    _timer = None
    _wrapped = False

    _level_prefix = {
        "INFO": "c",
        "DEBUG": "d",
        "VARIABLE": "v",
        "ANSWER": "a",
        "SOLUTION": "s",
        "WARNING": "w",
        "ERROR": "e",
    }

    @classmethod
    def _init(cls):
        """
        Initialize logger and timer, configure handlers and formatters,
        and register custom log levels (VARIABLE, ANSWER, SOLUTION).
        """
        if cls._logger is None:
            cls._timer = Timer()

            cls._logger = logging.getLogger("heulingo_logger")

            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)
            stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)

            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setLevel(logging.WARNING)

            formatter = cls._CustomFormatter()
            stdout_handler.setFormatter(formatter)
            stderr_handler.setFormatter(formatter)

            cls._logger.addHandler(stdout_handler)
            cls._logger.addHandler(stderr_handler)

            cls._add_custom_level("VARIABLE", 25)
            cls._add_custom_level("ANSWER", 26)
            cls._add_custom_level("SOLUTION", 27)

    @classmethod
    def _add_custom_level(cls, level_name: str, level_num: int) -> None:
        """
        Add custom log level to logging module.

        :param level_name: Name of custom log level.
        :type level_name: str
        :param level_num: Numeric value for custom log level.
        :type level_num: int
        """
        logging.addLevelName(level_num, level_name)

        def log_for_level(self, *args, **kwargs):
            if self.isEnabledFor(level_num):
                msg = " ".join(str(arg) for arg in args)
                self._log(level_num, msg, (), **kwargs)

        setattr(logging.Logger, level_name.lower(), log_for_level)

    @classmethod
    def set_level(cls, level: int):
        """
        Set log level for logger.

        :param level: Numeric value for log level.
        :type level: int
        """
        if cls._logger is None:
            cls._init()
        cls._logger.setLevel(level)

    @classmethod
    def get_logger(cls):
        """
        Get initialized and wrapped logger.
        """
        if cls._logger is None:
            cls._init()

        if not cls._wrapped:
            def wrap_method(method):
                def wrapper(*args, **kwargs):
                    msg = " ".join(str(arg) for arg in args)
                    return method(msg, **kwargs)
                return wrapper

            cls._logger.info = wrap_method(cls._logger.info)
            cls._logger.debug = wrap_method(cls._logger.debug)
            cls._logger.warning = wrap_method(cls._logger.warning)
            cls._logger.error = wrap_method(cls._logger.error)
            cls._logger.critical = wrap_method(cls._logger.critical)

            cls._wrapped = True

        return cls._logger

    class _CustomFormatter(logging.Formatter):
        """
        Custom formatter that formats log message with level prefix and elapsed time.
        """
        def format(self, record: logging.LogRecord) -> str:
            """
            Format log message with level prefix and elapsed time.

            :param record: LogRecord object.
            :type record: logging.LogRecord
            :return: Formatted log message string.
            :rtype: str
            """
            elapsed = f"{HeulingoLogger._timer.elapsed():.3f}s"
            prefix = HeulingoLogger._level_prefix[record.levelname]
            return f"{prefix} [{elapsed}] {record.getMessage()}"

logger = HeulingoLogger.get_logger()