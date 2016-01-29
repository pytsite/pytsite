"""Tumblr Init.
"""
from ._session import AuthSession, Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import reg, lang, assetman, content_export
    from ._content_export import Driver as ContentExportDriver

    app_key = reg.get('tumblr.app_key')
    if not app_key:
        raise Exception("Configuration parameter 'tumblr.app_key' is not defined.")

    app_secret = reg.get('tumblr.app_secret')
    if not app_secret:
        raise Exception("Configuration parameter 'tumblr.app_secret' is not defined.")

    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Register Content Export driver
    content_export.register_driver(ContentExportDriver())

__init()
