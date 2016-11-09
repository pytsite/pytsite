"""PytSite Plugin Manager.
"""
# Public API
from ._api import get_info, install, uninstall, is_installed, start

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import mkdir, path
    from pytsite import reg, settings, lang, assetman, permissions, http_api
    from . import _settings_form

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Create 'app.plugins' package
    plugins_path = reg.get('paths.plugins')
    if not path.exists(plugins_path):
        mkdir(plugins_path, 0o755)
        with open(plugins_path + path.sep + '__init__.py', 'wt') as f:
            f.write('"""Pytsite Application Plugins.\n"""\n')

    # Permissions
    permissions.define_permission('pytsite.plugman.manage', 'pytsite.plugman@plugin_management', 'app')

    # Settings
    settings.define('plugman', _settings_form.Form, 'pytsite.plugman@plugins', 'fa fa-cubes', 'pytsite.plugman.manage')

    # HTTP API
    http_api.register_handler('plugman', 'pytsite.plugman.http_api')

    # Install required plugins
    for p_name in reg.get('plugins', ()):
        if is_installed(p_name):
            continue

        install(p_name)

    # Start installed plugins
    for p_name, p_info in get_info().items():
        if p_info['installed_version']:
            start(p_name)


_init()
