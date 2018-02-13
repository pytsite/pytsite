"""PytSite Queue API Functions
"""
from pytsite import cache as _cache, util as _util, threading as _threading
from typing import Any as _Any

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_POOL = _cache.create_pool('pytsite.queue')


class Task:
    def __init__(self, handler: str, args):
        self._handler = _util.get_module_attr(handler)
        self.args = args

    def exec(self):
        self._handler(self.args)


class Queue:
    def __init__(self, name: str):
        """Init
        """
        self._name = name

    def put(self, handler: str, args: _Any = None):
        """Put a task into the queue
        """
        _POOL.l_push(self._name, {
            'handler': handler,
            'args': args,
        })

        return self

    def execute(self, blocking_mode: bool = False):
        """Execute all pending tasks
        """

        def _execute():
            for t in self:
                t.exec()

        _threading.run_in_thread(_execute) if not blocking_mode else _execute()

        return self

    def __iter__(self):
        return self

    def __next__(self) -> Task:
        """Get next pending task
        """
        try:
            return Task(**_POOL.r_pop(self._name))
        except _cache.error.KeyNotExist:
            raise StopIteration()
