"""PytSite Theme Package
"""
from . import _error as error
from ._api import themes_path, register, get_registered, switch, get, load, install

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import listdir, path, makedirs
    from pytsite import permissions, settings, lang, router, assetman, http_api, tpl, file
    from . import _settings_form, _eh, _http_api_controllers

    # Register translations
    lang.register_package(__name__)

    # Register assetman package and tasks
    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.js_module('pytsite-theme-widget-themes-browser', 'pytsite.theme@js/themes-browser')

    # App's logo URL resolver
    def logo_url(width: int = 50, height: int = 50):
        s = settings.get('theme.logo_fid')
        return file.get(s).get_url(width=width, height=height) if s else assetman.url('$theme@img/appicon.png')

    # Tpl globals
    tpl.register_global('theme_logo_url', logo_url)

    # Permissions
    permissions.define_permission('pytsite.theme.manage', 'pytsite.theme@manage_themes', 'app')

    # Settings
    settings.define('theme', _settings_form.Form, 'pytsite.theme@appearance', 'fa fa-paint-brush',
                    'pytsite.theme.manage')

    # Event listeners
    router.on_dispatch(_eh.router_dispatch)

    # HTTP API handlers
    http_api.handle('POST', 'theme', _http_api_controllers.Install(), 'pytsite.theme@install')
    http_api.handle('PATCH', 'theme', _http_api_controllers.Switch(), 'pytsite.theme@switch')
    http_api.handle('DELETE', 'theme', _http_api_controllers.Uninstall(), 'pytsite.theme@uninstall')

    # Create themes directory
    t_path = themes_path()
    if not path.isdir(t_path):
        makedirs(t_path, 0o755)

    # Register all themes found in the themes directory
    for name in sorted(listdir(t_path)):
        if not path.isdir(t_path) or name.startswith('_') or name.startswith('.'):
            continue

        register('themes.' + name)


_init()
