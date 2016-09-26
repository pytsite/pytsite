"""PytSite FB Init.
"""
# Public API
from ._session import AuthSession, Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import lang, assetman, content_export, router, tpl, comments, events, permissions, settings
    from . import _eh, _settings_form
    from ._content_export import Driver as ContentExportDriver
    from ._comments import Driver

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)

    # Routes
    router.add_rule('/fb/authorize', 'pytsite.fb@authorize')

    # Content export driver
    content_export.register_driver(ContentExportDriver())

    # Comments driver
    comments.register_driver(Driver())

    # Register settings form
    permissions.define_permission('fb.settings.manage', 'pytsite.fb@manage_fb_settings', 'app')
    settings.define('fb', _settings_form.Form, 'pytsite.fb@facebook', 'fa fa-facebook', 'fb.settings.manage')

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


__init()
