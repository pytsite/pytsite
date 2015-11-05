"""PytSite FB Init.
"""
from ._session import AuthSession, Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import reg, lang, assetman, content_export, router
    from ._content_export import Driver as ContentExportDriver

    app_id = reg.get('fb.app_id')
    if not app_id:
        raise Exception("Configuration parameter 'fb.app_id' is not defined.")

    app_secret = reg.get('fb.app_secret')
    if not app_secret:
        raise Exception("Configuration parameter 'fb.app_secret' is not defined.")

    lang.register_package(__name__)
    assetman.register_package(__name__)

    content_export.register_driver('fb', 'pytsite.fb@facebook', ContentExportDriver)

    # Routes
    router.add_rule('/fb/authorize', 'pytsite.fb.ep.authorize')


__init()
