"""PytSite Thread
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Callable, Any
from threading import Timer as PythonTimer, current_thread


class Timer(PythonTimer):
    @property
    def parent(self):
        """Get parent thread

        :rtype: Timer
        """
        return self._parent

    def __init__(self, interval: float, function: Callable[..., Any], args: list = None, kwargs: dict = None):
        """Init
        """
        super().__init__(interval, function, args, kwargs)

        self._parent = current_thread()
