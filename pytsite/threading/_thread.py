"""PytSite Thread
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from threading import Thread as PythonThread, current_thread


class Thread(PythonThread):
    @property
    def parent(self):
        """Get parent thread

        :rtype: Thread
        """
        return self._parent

    def __init__(self, *args, **kwargs):
        """Init
        """
        super().__init__(*args, **kwargs)

        self._parent = current_thread()
