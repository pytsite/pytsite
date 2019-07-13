"""PytSite Update Console Command
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pickle
import subprocess
from os import path, chdir
from semaver import Version
from pytsite import console, events, lang, package_info, reg, maintenance, reload, pip

_DEBUG = reg.get('debug')


def _subprocess_run(cmd: list):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if r.returncode != 0:
        console.print_warning(r.stderr.decode('utf-8'))

    if _DEBUG and r.stdout:
        console.print_info(r.stdout.decode('utf-8'))


class Update(console.Command):
    """Update Console Command
    """

    def __init__(self):
        super().__init__()
        self.define_option(console.option.Bool('debug', default=_DEBUG))
        self.define_option(console.option.PositiveInt('stage', default=1, maximum=4))
        self.define_option(console.option.PositiveInt('stop-after', default=0, maximum=4))

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
        app_path = reg.get('paths.app')
        config_path = reg.get('paths.config')
        stage = self.opt('stage')
        stop_after = self.opt('stop-after')

        chdir(app_path)
        maintenance.enable()

        d = self._get_update_data()
        if not d['update_in_progress']:
            d['pytsite_version_from'] = str(package_info.version('pytsite'))
            d['app_version_from'] = str(package_info.version('app'))
            d['update_in_progress'] = True
            self._set_update_data(d)

        # Stage 1: update pip and PytSite
        if stage == 1:
            console.print_info(lang.t('pytsite.update@updating_environment'))

            # Update pip
            pip.install('pip', None, True, self.opt('debug'))

            # Update PytSite
            pip.install('pytsite', package_info.requires_pytsite('app'), True, self.opt('debug'))

            d['pytsite_version_to'] = str(package_info.version('pytsite', False))
            self._set_update_data(d)

            # Notify listeners
            events.fire('pytsite.update@stage_1')

            if stop_after != 1:
                subprocess.call(['./console', 'update', '--stage=2'])
            else:
                maintenance.disable()

        # Stage 2: update application and configuration
        elif stage == 2:
            # Notify listeners about PytSite update
            events.fire('pytsite.update@pytsite', v_from=Version(d['pytsite_version_from']))

            # Update configuration
            if path.exists(path.join(config_path, '.git')):
                console.print_info(lang.t('pytsite.update@updating_configuration'))
                _subprocess_run(['git', '-C', config_path, 'pull'])

            # Update application
            if path.exists(path.join(app_path, '.git')):
                console.print_info(lang.t('pytsite.update@updating_application'))
                _subprocess_run(['git', '-C', app_path, 'pull'])
            d['app_version_to'] = str(package_info.version('app', False))
            self._set_update_data(d)

            # Notify listeners
            events.fire('pytsite.update@stage_2')

            if stop_after != 2:
                subprocess.call(['./console', 'update', '--stage=3'])
            else:
                maintenance.disable()

        # Stage 3: finish update process
        elif stage == 3:
            console.print_info(lang.t('pytsite.update@applying_updates'))

            # Notify listeners about application update
            events.fire('pytsite.update@app', v_from=Version(d['app_version_from']))

            # Notify listeners
            events.fire('pytsite.update@update')

            # Application's update hook
            import app
            if hasattr(app, 'app_update') and callable(app.app_update):
                app.app_update(v_from=Version(d['app_version_from']))

            # Mark that update was finished successfully
            d['update_in_progress'] = False
            self._set_update_data(d)

            # Disable maintenance mode
            maintenance.disable()

            # Reload the application
            reload.reload()

    @property
    def _data_path(self) -> str:
        return path.join(reg.get('paths.storage'), 'pytsite.update')

    def _get_update_data(self) -> dict:
        """Get current update state.
        """
        data = {}

        if path.exists(self._data_path):
            with open(self._data_path, 'rb') as f:
                data = pickle.load(f)

            if not isinstance(data, dict):
                data = {}

        if not data:
            pytsite_v = str(package_info.version('pytsite'))
            app_v = str(package_info.version('app'))
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
            pickle.dump(data, f)
