"""PytSite Update Console Command
"""
import pickle as _pickle
import subprocess as _subprocess
from os import path as _path, chdir as _chdir
from pytsite import console as _console, events as _events, lang as _lang, package_info as _package_info, reg as _reg, \
    logger as _logger, maintenance as _maintenance, util as _util, reload as _reload

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Update(_console.Command):
    """Update Console Command
    """

    def __init__(self):
        super().__init__()
        self.define_option(_console.option.PositiveInt('stage', default=1, maximum=3))
        self.define_option(_console.option.PositiveInt('stop-after', default=0, maximum=3))

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
        config_path = _reg.get('paths.config')
        stage = self.opt('stage')
        stop_after = self.opt('stop-after')

        _chdir(app_path)
        _maintenance.enable()

        if stage == 1:
            # Update pip and pytsite
            _console.print_info(_lang.t('pytsite.update@updating_environment'))
            _subprocess.call(['pip', 'install', '-U', 'pip'])
            _subprocess.call(['pip', 'install', '-U', 'pytsite'])

            _logger.info('pytsite.update@stage_1 event, PytSite version: {}'.format(_package_info.version('pytsite')))
            _events.fire('pytsite.update@stage_1')

            if stop_after != 1:
                _subprocess.call(['./console', 'update', '--stage=2'])
            else:
                _maintenance.disable()

        elif stage == 2:
            # Update configuration, if applicable
            if _path.exists(_path.join(config_path, '.git')):
                _console.print_info(_lang.t('pytsite.update@updating_configuration'))
                _subprocess.call(['git', '-C', config_path, 'pull'])

            # Update application, if applicable
            if _path.exists(_path.join(app_path, '.git')):
                _console.print_info(_lang.t('pytsite.update@updating_application'))
                _subprocess.call(['git', '-C', app_path, 'pull'])

            _logger.info('pytsite.update@stage_2 event, PytSite version: {}'.format(_package_info.version('pytsite')))
            _events.fire('pytsite.update@stage_2')

            if stop_after != 2:
                _subprocess.call(['./console', 'update', '--stage=3'])
            else:
                _maintenance.disable()

        elif stage == 3:
            _console.print_info(_lang.t('pytsite.update@applying_updates'))

            state = self._get_state()
            curent_version = _package_info.version('pytsite')
            stop = False
            for major in range(0, 100):
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
                        if major_minor_rev == curent_version:
                            stop = True

                        # Update is already applied
                        if major_minor_rev in state:
                            continue

                        # Notify listeners
                        _logger.info('pytsite.update event, version={}'.format(major_minor_rev))
                        _events.fire('pytsite.update', version=major_minor_rev)
                        _events.fire('pytsite.update@{}'.format(major_minor_rev.replace('.', '_')))

                        # Saving number as applied update
                        state.add(major_minor_rev)

            self._save_state(state)

            # Update required pip packages by application and theme
            for pkg_name in ['app']:
                for pip_pkg_spec in _package_info.requires_packages(pkg_name):
                    _console.print_info(_lang.t('pytsite.update@updating_pip_package', {'package': pip_pkg_spec}))
                    try:
                        _util.install_pip_package(pip_pkg_spec, True)
                    except _util.error.PipPackageInstallError as e:
                        raise _console.error.Error(e)

            _logger.info('pytsite.update@after event')
            _events.fire('pytsite.update@after')

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
