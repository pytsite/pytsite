"""PytSite Update Console Command
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle as _pickle
import subprocess as _subprocess
from os import path as _path, chdir as _chdir
from pytsite import console as _console, events as _events, lang as _lang, package_info as _package_info, reg as _reg, \
    maintenance as _maintenance, reload as _reload, pip as _pip, semver as _semver

_DEBUG = _reg.get('debug')


def _subprocess_run(cmd: list):
    r = _subprocess.run(cmd, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE)

    if r.returncode != 0:
        _console.print_warning(r.stderr.decode('utf-8'))

    if _DEBUG and r.stdout:
        _console.print_info(r.stdout.decode('utf-8'))


class Update(_console.Command):
    """Update Console Command
    """

    def __init__(self):
        super().__init__()
        self.define_option(_console.option.PositiveInt('stage', default=1, maximum=4))
        self.define_option(_console.option.PositiveInt('stop-after', default=0, maximum=4))

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

        d = self._get_update_data()
        if not d['update_in_progress']:
            d['pytsite_version_from'] = _package_info.version('pytsite')
            d['app_version_from'] = _package_info.version('app')
            d['update_in_progress'] = True
            self._set_update_data(d)

        # Stage 1: update pip and PytSite
        if stage == 1:
            _console.print_info(_lang.t('pytsite.update@updating_environment'))

            # Update pip
            out = _pip.install('pip', True)
            if _DEBUG:
                _console.print_normal(out)

            # Update PytSite files
            out = _pip.install('pytsite', True)
            if _DEBUG:
                _console.print_normal(out)
            d['pytsite_version_to'] = _package_info.version('pytsite', False)
            self._set_update_data(d)

            # Notify listeners
            _events.fire('pytsite.update@stage_1')

            if stop_after != 1:
                _subprocess.call(['./console', 'update', '--stage=2'])
            else:
                _maintenance.disable()

        # Stage 2: update application and configuration
        elif stage == 2:
            # Notify listeners about PytSite update
            _events.fire('pytsite.update@pytsite', v_from=_semver.Version(d['pytsite_version_from']))

            # Update configuration
            if _path.exists(_path.join(config_path, '.git')):
                _console.print_info(_lang.t('pytsite.update@updating_configuration'))
                _subprocess_run(['git', '-C', config_path, 'pull'])

            # Update application
            if _path.exists(_path.join(app_path, '.git')):
                _console.print_info(_lang.t('pytsite.update@updating_application'))
                _subprocess_run(['git', '-C', app_path, 'pull'])
            d['app_version_to'] = _package_info.version('app', False)
            self._set_update_data(d)

            # Notify listeners
            _events.fire('pytsite.update@stage_2')

            if stop_after != 2:
                _subprocess.call(['./console', 'update', '--stage=3'])
            else:
                _maintenance.disable()

        # Stage 3: finish update process
        elif stage == 3:
            _console.print_info(_lang.t('pytsite.update@applying_updates'))

            # Notify listeners about application update
            _events.fire('pytsite.update@app', v_from=_semver.Version(d['app_version_from']))

            # Notify listeners
            _events.fire('pytsite.update@update')

            # Application's update hook
            import app
            if hasattr(app, 'app_update') and callable(app.app_update):
                app.app_update(v_from=_semver.Version(d['app_version_from']))

            # Mark that update was finished successfully
            d['update_in_progress'] = False
            self._set_update_data(d)

            # Disable maintenance mode
            _maintenance.disable()

            # Reload the application
            _reload.reload()

    @property
    def _data_path(self) -> str:
        return _path.join(_reg.get('paths.storage'), 'pytsite.update')

    def _get_update_data(self) -> dict:
        """Get current update state.
        """
        data = {}

        if _path.exists(self._data_path):
            with open(self._data_path, 'rb') as f:
                data = _pickle.load(f)

            if not isinstance(data, dict):
                data = {}

        if not data:
            pytsite_v = _package_info.version('pytsite')
            app_v = _package_info.version('app')
            data = {
                'pytsite_version_from': pytsite_v,
                'pytsite_version_to': pytsite_v,
                'app_version_from': app_v,
                'app_version_to': app_v,
                'update_in_progress': False,
            }

        return data

    def _set_update_data(self, data: dict):
        """Save current update state.
        """
        with open(self._data_path, 'wb') as f:
            _pickle.dump(data, f)
