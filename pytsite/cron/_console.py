"""PytSite Cron Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console
from ._worker import EVENT_NAMES, worker


class Run(console.Command):
    @property
    def name(self) -> str:
        return 'cron:run'

    @property
    def description(self) -> str:
        return 'pytsite.cron@run_console_command_description'

    @property
    def signature(self) -> str:
        return f'{self.name} ' + '|'.join(EVENT_NAMES)

    def exec(self):
        evt = self.arg(0)

        if not evt:
            raise console.error.MissingArgument()

        if evt not in EVENT_NAMES:
            raise console.error.InvalidArgument(0, evt)

        worker(evt, False, True)
