"""PytSite Update Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle as _pickle
from os import path as _path
from pytsite import console as _console, events as _events, lang as _lang, version as _pytsite_ver, reg as _reg, \
    logger as _logger, maintenance as _maintenance


class Update(_console.command.Abstract):
    """Setup Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'update'

    def get_description(self) -> str:
        """Get description of the command.
        """
        return _lang.t('pytsite.update@update_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        state = self._get_state()
        cur_ver = _pytsite_ver()
        cur_ver_str = '{}.{}.{}'.format(cur_ver[0], cur_ver[1], cur_ver[2])

        _maintenance.enable()

        stop = False
        for major in range(0, 1):
            if stop:
                break
            for minor in range(0, 100):
                if stop:
                    break
                for rev in range(0, 10):
                    if stop:
                        break

                    major_minor_rev = '{}.{}.{}'.format(major, minor, rev)

                    # Current version reached
                    if major_minor_rev == cur_ver_str:
                        stop = True

                    # Update is already applied
                    if major_minor_rev in state:
                        continue

                    # Notify listeners
                    _logger.info('pytsite.update event, version={}'.format(major_minor_rev), __name__)
                    _events.fire('pytsite.update', version=major_minor_rev)

                    # Saving number as applied update
                    state.add(major_minor_rev)

        _logger.info('pytsite.update.after event', __name__)
        _events.fire('pytsite.update.after')

        self._save_state(state)
        _maintenance.disable()

        # _events.fire('pytsite.update')

    def _get_state(self) -> set:
        data = set()

        data_path = self._get_data_path()
        if not _path.exists(data_path):
            return data
        else:
            with open(data_path, 'rb') as f:
                data = _pickle.load(f)

        return data

    def _save_state(self, state: set):
        with open(self._get_data_path(), 'wb') as f:
            _pickle.dump(state, f)

    @staticmethod
    def _get_data_path() -> str:
        return _path.join(_reg.get('paths.storage'), 'update.data')
