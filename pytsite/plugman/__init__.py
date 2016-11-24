"""PytSite Plugin Manager.
"""
# Public API
from . import _error as error
from ._api import get_plugins_path, get_info, get_info_dev, install, uninstall, is_installed, start, is_started

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import mkdir, path
    from pytsite import reg, settings, lang, assetman, permissions, http_api, logger, events
    from . import _settings_form, _eh

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Create 'plugins' package
    plugins_path = get_plugins_path()
    if not path.exists(plugins_path):
        mkdir(plugins_path, 0o755)
        with open(path.join(plugins_path, '__init__.py'), 'wt') as f:
            f.write('"""Pytsite Application Plugins.\n"""\n')

    # Permissions
    permissions.define_permission('pytsite.plugman.manage', 'pytsite.plugman@plugin_management', 'app')

    # Settings
    settings.define('plugman', _settings_form.Form, 'pytsite.plugman@plugins', 'fa fa-plug', 'pytsite.plugman.manage')

    # HTTP API
    http_api.register_handler('plugman', 'pytsite.plugman.http_api')

    # Event handlers
    events.listen('pytsite.update', _eh.update)

    # Install required plugins
    for p_name in reg.get('plugins', ()):
        if is_installed(p_name):
            continue

        install(p_name)

    try:
        # Start installed plugins
        for p_name, p_info in get_info().items():
            if p_info['installed_version']:
                start(p_name)

        # Start plugins in development
        for p_name in get_info_dev():
            if not is_started(p_name):
                start(p_name, True)

    except error.PluginStartError as e:
        logger.error(e, exc_info=e)


_init()
