"""PytSite Theme Package.
"""
# Public API
from . import _error as error
from ._api import get_themes_path, register, get_list, get_current, set_current, is_registered, get_theme_settings, \
    get_info, load

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import listdir, path, makedirs
    from pytsite import permissions, settings, lang, events, router, assetman, http_api
    from . import _settings_form, _eh, _http_api

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Permissions
    permissions.define_permission('pytsite.theme.manage', 'pytsite.theme@manage_themes', 'app')

    # Settings
    settings.define('theme', _settings_form.Form, 'pytsite.theme@theme', 'fa fa-paint-brush', 'pytsite.theme.manage')

    # Event listeners
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.update', _eh.update)

    # HTTP API handlers
    http_api.handle('GET', 'theme/settings/<theme_package_name>', _http_api.get_settings, 'pytsite.theme@get_settings')

    # Default home page handler
    router.add_rule('/', '$theme@home')

    # Initialize themes
    themes_path = get_themes_path()

    if not path.isdir(themes_path):
        makedirs(themes_path, 0o755)

    for name in sorted(listdir(themes_path)):
        if not path.isdir(themes_path) or name.startswith('_') or name.startswith('.'):
            continue

        register('themes.' + name)

    # Set current theme from settings or keep previous if settings are absent
    set_current(settings.get('theme.current_theme', get_current()))


_init()
