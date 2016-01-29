"""PytSite LiveJournal Package.
"""
# Public API
from ._session import Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import lang, assetman, content_export
    from ._content_export import Driver as ContentExportDriver

    # Register resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Register Content Export driver
    content_export.register_driver(ContentExportDriver())


__init()
