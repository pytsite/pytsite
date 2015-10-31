"""Reddit Init.
"""
from ._session import AuthSession, Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import reg, lang, assetman, content_export, router
    from ._content_export import Driver as ContentExportDriver

    app_key = reg.get('reddit.app_key')
    if not app_key:
        raise Exception("Configuration parameter 'reddit.app_key' is not defined.")

    app_secret = reg.get('reddit.app_secret')
    if not app_secret:
        raise Exception("Configuration parameter 'reddit.app_secret' is not defined.")

    # Resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Register Content Export driver
    content_export.register_driver('reddit', __name__ + '@reddit', ContentExportDriver)

    # Routes
    router.add_rule('/reddit/authorize', 'pytsite.reddit.ep.authorize')

__init()
