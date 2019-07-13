"""PytSite Queue API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import cache, util, threading
from typing import Any, Union, Callable

_POOL = cache.create_pool('pytsite.queue')


class Task:
    def __init__(self, handler: str, *args, **kwargs):
        if isinstance(handler, str):
            handler = util.get_module_attr(handler)

        self._handler = handler
        self._args = args
        self._kwargs = kwargs

    def exec(self):
        self._handler(*self._args, **self._kwargs)


class Queue:
    def __init__(self, name: str):
        """Init
        """
        self._name = name

    def put(self, handler: Union[Callable[..., Any], str], *args, **kwargs):
        """Put a task into the queue
        """
        if not (callable(handler) or isinstance(handler, str)):
            raise TypeError('Callable or string expected, got {}'.format(type(handler)))

        _POOL.list_l_push(self._name, (handler, args, kwargs))

        return self

    def execute(self, wait: bool = False):
        """Execute all pending tasks
        """
        threads = []
        for task in self:
            threads.append(threading.run_in_thread(task.exec))

        # Wait while all tasks finish
        if wait:
            for thread in threads:
                thread.join()

        return self

    def __iter__(self):
        return self

    def __next__(self) -> Task:
        """Get next pending task
        """
        try:
            t_data = _POOL.list_r_pop(self._name)
            if len(t_data) == 3:
                return Task(t_data[0], *t_data[1], **t_data[2])
            elif len(t_data) == 2:
                return Task(t_data[0], *t_data[1])
            else:
                return Task(t_data[0])
        except cache.error.KeyNotExist:
            raise StopIteration()
