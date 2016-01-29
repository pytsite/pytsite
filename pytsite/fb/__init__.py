"""PytSite FB Init.
"""
# Public API
from ._session import AuthSession, Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import reg, lang, assetman, content_export, router, tpl, comments, events
    from . import _eh
    from ._content_export import Driver as ContentExportDriver
    from ._comments import Driver

    # App ID is mandatory configuration parameter
    app_id = reg.get('fb.app_id')
    if not app_id:
        raise Exception("Configuration parameter 'fb.app_id' is not defined.")

    # App secret is mandatory configuration parameter
    app_secret = reg.get('fb.app_secret')
    if not app_secret:
        raise Exception("Configuration parameter 'fb.app_secret' is not defined.")

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)

    # Routes
    router.add_rule('/fb/authorize', 'pytsite.fb.ep.authorize')

    # Content export driver
    content_export.register_driver(ContentExportDriver())

    # Comments driver
    comments.register_driver(Driver())

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


__init()
