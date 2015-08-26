"""PytSite Twitter Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import content_export
    from pytsite import assetman
    from pytsite import lang
    from ._content_export import Driver as ContentExportDriver

    # Register resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Register Content Export driver
    content_export.register_driver('twitter', __name__ + '@twitter', ContentExportDriver)

__init()
