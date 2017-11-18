"""PytSite Theme Package
"""
from . import _error as error
from ._api import themes_path, register, get_registered, switch, get, load, install

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import listdir, path, makedirs
    from pytsite import permissions, settings, lang, router, assetman, http_api, tpl, file, odm
    from . import _settings_form, _eh, _http_api_controllers, _model

    # Translations
    lang.register_package(__name__)
    lang.on_translate(_eh.lang_translate)

    # Register assetman package and tasks
    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.t_less(__name__ + '@**')
    assetman.js_module('pytsite-theme-widget-themes-browser', 'pytsite.theme@js/themes-browser')
    assetman.js_module('pytsite-theme-widget-translations-edit', 'pytsite.theme@js/translations-edit')

    # App's logo URL resolver
    def logo_url(width: int = 0, height: int = 0):
        s = settings.get('theme.logo')
        try:
            return file.get(s).get_url(width=width, height=height) if s else assetman.url('$theme@img/appicon.png')
        except file.error.FileNotFound:
            return assetman.url('$theme@img/appicon.png')

    # Tpl globals
    tpl.register_global('theme_logo_url', logo_url)

    # Permissions
    permissions.define_permission('pytsite.theme.manage', 'pytsite.theme@manage_themes', 'app')

    # ODM models
    odm.register_model('theme_translation', _model.Translation)

    # Settings
    settings.define('theme', _settings_form.Form, 'pytsite.theme@appearance', 'fa fa-paint-brush',
                    'pytsite.theme.manage')

    # Event listeners
    router.on_dispatch(_eh.router_dispatch)

    # HTTP API handlers
    http_api.handle('POST', 'theme', _http_api_controllers.Install(), 'pytsite.theme@install')
    http_api.handle('PATCH', 'theme', _http_api_controllers.Switch(), 'pytsite.theme@switch')
    http_api.handle('DELETE', 'theme', _http_api_controllers.Uninstall(), 'pytsite.theme@uninstall')

    # Create themes directory structure
    themes_dir = themes_path()
    if not path.isdir(themes_dir):
        # Create themes directory
        makedirs(themes_dir, 0o755)

        # Create default theme directory
        theme_dir = path.join(themes_dir, 'default')
        makedirs(theme_dir, 0o755)

        # Create __init__.py
        with open(path.join(theme_dir, '__init__.py'), 'wt') as f:
            f.write('"""Default Theme\n"""\n')

        # Create 'theme.json'
        with open(path.join(theme_dir, 'theme.json'), 'wt') as f:
            f.write(
                '{\n'
                '  "name": "default",\n'
                '  "version": "0.1",\n'
                '  "description": {\n'
                '    "en": "Default Theme"\n'
                '  },\n'
                '  "author": {\n'
                '    "name": "John Doe",\n'
                '    "email": "john@doe.com",\n'
                '    "url": "https://john-doe.com"\n'
                '  },\n'
                '  "requires": {\n'
                '    "packages": [],\n'
                '    "plugins": []\n'
                '  }\n'
                '}\n'
            )

        # Create '.gitignore'
        with open(path.join(theme_dir, '.gitignore'), 'wt') as f:
            f.write('__pycache__\n')

    # Register all themes found in the themes directory
    for name in sorted(listdir(themes_dir)):
        if not path.isdir(themes_dir) or name.startswith('_') or name.startswith('.'):
            continue

        register('themes.' + name)


_init()
