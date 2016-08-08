"""PytSite Profiler API.
"""
import cProfile as _cProfile
import pstats as _pstats
from pytsite import threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Thread safe profiler objects
_profilers = {}


def enable(subcalls: bool = True, builtins: bool = True):
    """Start profiling.
    """
    tid = _threading.get_id()
    if tid not in _profilers:
        _profilers[tid] = _cProfile.Profile()

    _profilers[tid].enable(subcalls, builtins)


def disable():
    """Stop profiling.
    """
    tid = _threading.get_id()
    if tid not in _profilers:
        raise RuntimeError('Unknown profiler.')

    _profilers[tid].disable()


def clear():
    """Clear collected information.
    """
    tid = _threading.get_id()
    if tid not in _profilers:
        raise RuntimeError('Unknown profiler.')

    _profilers[tid].clear()


def print_stats(filename: str, mode: str = 'w', header: str = None, sort_by: str = 'cumtime'):
    """Print collected statistic into file.
    """
    tid = _threading.get_id()
    if tid not in _profilers:
        raise RuntimeError('Unknown profiler.')

    with open(filename, mode) as f:
        if header:
            f.write("{}\n".format(header))

        ps = _pstats.Stats(_profilers[tid], stream=f)
        ps.sort_stats(sort_by)
        ps.print_stats()
