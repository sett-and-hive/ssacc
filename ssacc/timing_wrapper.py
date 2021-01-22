"""
Timing wraper

These references helped:
https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator
    Use wrapping from functools to improve Matt Alcock's answer.
https://realpython.com/primer-on-python-decorators/#timing-functions
"""

import functools
import time


def timing(func):
    """Print the runtime of the decorated function."""

    @functools.wraps(functools)
    def wrapper_timing(*args, **kw):
        """Timing wrapper."""
        start_time = time.perf_counter()
        result = func(*args, **kw)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f}")
        return result

    wrapper_timing.__name__ = func.__name__
    wrapper_timing.__doc__ = func.__doc__
    return wrapper_timing
