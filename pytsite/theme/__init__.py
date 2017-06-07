"""PytSite Theme Package.
"""
# Public API
from . import _error as error
from ._api import get_themes_path, register, get_registered, switch, get, load

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import listdir, path, makedirs
    from pytsite import permissions, settings, lang, events, router, assetman, http_api, tpl, file
    from . import _settings_form, _eh, _http_api

    # Resources
    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')

    # App's logo URL resolver
    def logo_url(width: int = 50, height: int = 50):
        s = settings.get('theme.logo_fid')
        return file.get(s).get_url(width=width, height=height) if s else assetman.url('$theme@img/appicon.png')

    # Tpl globals
    tpl.register_global('theme_logo_url', logo_url)

    # Permissions
    permissions.define_permission('pytsite.theme.manage', 'pytsite.theme@manage_themes', 'app')

    # Settings
    settings.define('theme', _settings_form.Form, 'pytsite.theme@theme', 'fa fa-paint-brush', 'pytsite.theme.manage')

    # Event listeners
    router.on_dispatch(_eh.router_dispatch)
    events.listen('pytsite.update', _eh.update)

    # HTTP API handlers
    http_api.handle('GET', 'theme/settings/<theme_package_name>', _http_api.get_settings, 'pytsite.theme@get_settings')

    # Default home page handler
    router.handle('/', '$theme@home', 'home')

    # Create themes directory
    themes_path = get_themes_path()
    if not path.isdir(themes_path):
        makedirs(themes_path, 0o755)

    # Register all themes found in the themes directory
    for name in sorted(listdir(themes_path)):
        if not path.isdir(themes_path) or name.startswith('_') or name.startswith('.'):
            continue

        register('themes.' + name)


_init()
