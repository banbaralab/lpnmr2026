import time

class Timer:
    """
    Timer to measure elapsed time since start.
    """
    def __init__(self):
        self._start_time = time.time()

    def elapsed(self) -> float:
        """
        Compute elapsed time since start.

        :return: Elapsed time since start.
        :rtype: float
        """
        return time.time() - self._start_time
    
    def restart(self) -> None:
        """
        Reset start time.
        """
        self._start_time = time.time()