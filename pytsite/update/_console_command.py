"""PytSite Update Console Commands
"""
import pickle as _pickle
import subprocess as _subprocess
from os import path as _path, chdir as _chdir
from pytsite import console as _console, events as _events, lang as _lang, core_version as _pytsite_ver, reg as _reg, \
    logger as _logger, maintenance as _maintenance, reload as _reload, theme as _theme

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Update(_console.Command):
    """Setup Command.
    """

    def __init__(self):
        super().__init__()
        self.define_option(_console.option.PositiveInt('stage', default=0, maximum=2))

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'update'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.update@update_console_command_description'

    def exec(self, args: tuple = (), **kwargs):
        """Execute the command.
        """
        app_path = _reg.get('paths.app')
        theme_path = _theme.get().path
        stage = self.opt('stage')

        _chdir(app_path)
        _maintenance.enable()

        if stage in (0, 1):
            # Update pip and pytsite
            _console.print_info(_lang.t('pytsite.update@updating_environment'))
            _subprocess.call(['pip', 'install', '-U', 'pip'])
            _subprocess.call(['pip', 'install', '-U', 'pytsite'])

            # Update application, if applicable
            if _path.exists(_path.join(app_path, '.git')):
                _console.print_info(_lang.t('pytsite.update@updating_application'))
                _subprocess.call(['git', '-C', app_path, 'pull'])

            if _path.exists(_path.join(theme_path, '.git')):
                _console.print_info(_lang.t('pytsite.update@updating_theme'))
                _subprocess.call(['git', '-C', theme_path, 'pull'])

            # Call second step automatically only if '--stage=1' option was not explicitly provided
            if stage == 0:
                _subprocess.call(['./console', 'update', '--stage=2'])
            else:
                _maintenance.disable()

        elif stage == 2:
            _console.print_info(_lang.t('pytsite.update@applying_updates'))

            state = self._get_state()
            cur_ver = _pytsite_ver()
            cur_ver_str = '{}.{}.{}'.format(cur_ver[0], cur_ver[1], cur_ver[2])
            stop = False
            for major in range(0, 1):
                if stop:
                    break
                for minor in range(0, 100):
                    if stop:
                        break
                    for rev in range(0, 100):
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
                        _logger.info('pytsite.update event, version={}'.format(major_minor_rev))
                        _events.fire('pytsite.update', version=major_minor_rev)

                        # Saving number as applied update
                        state.add(major_minor_rev)

            self._save_state(state)

            _logger.info('pytsite.update.after event')
            _events.fire('pytsite.update.after')

            # Disable maintenance mode
            _maintenance.disable()

            # Reload the application
            _reload.reload()

    def _get_state(self) -> set:
        """Get current update state.
        """
        data = set()

        data_path = self._get_data_path()
        if not _path.exists(data_path):
            return data
        else:
            with open(data_path, 'rb') as f:
                data = _pickle.load(f)

        return data

    def _save_state(self, state: set):
        """Save current update state.
        """
        with open(self._get_data_path(), 'wb') as f:
            _pickle.dump(state, f)

    @staticmethod
    def _get_data_path() -> str:
        return _path.join(_reg.get('paths.storage'), 'update.data')
