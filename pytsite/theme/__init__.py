"""PytSite Theme Package.
"""
# Public API
from . import _error as error
from ._api import get_themes_path, register, get_list, get_current, set_current, is_registered

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import listdir, path
    from pytsite import permissions, settings, lang, events, router
    from . import _settings_form, _eh

    # Resources
    lang.register_package(__name__)

    # Permissions
    permissions.define_permission('pytsite.theme.manage', 'pytsite.theme@manage_themes', 'app')

    # Settings
    settings.define('theme', _settings_form.Form, 'pytsite.theme@themes', 'fa fa-paint-brush', 'pytsite.theme.manage')

    # Event listeners
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.update', _eh.update)

    # Default home page handler
    router.add_rule('/', '$theme@home')

    # Initialize themes
    themes_path = get_themes_path()
    if path.isdir(themes_path):
        for name in sorted(listdir(themes_path)):
            if not path.isdir(path.join(themes_path, name)) or name.startswith('_') or name.startswith('.'):
                continue

            try:
                register('themes.' + name)
            except ImportError:
                pass


_init()
