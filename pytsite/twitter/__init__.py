"""PytSite Twitter Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import reg, content_export, assetman, lang
    from ._content_export import Driver as ContentExportDriver

    # Checking settings
    if not reg.get('twitter.app_key'):
        raise Exception("Configuration parameter 'twitter.app_key' should be defined.")
    if not reg.get('twitter.app_secret'):
        raise Exception("Configuration parameter 'twitter.app_secret' should be defined.")

    # Register resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Register Content Export driver
    content_export.register_driver(ContentExportDriver())

__init()
