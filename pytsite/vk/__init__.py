"""PytSite VK Package.
"""
from ._session import Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import content_export, assetman, lang, reg, events
    from . import _eh
    from ._content_export import Driver as ContentExportDriver

    if not reg.get('vk.app_id'):
        raise Exception("'vk.app_id' configuration option should be defined.")

    if not reg.get('vk.app_secret'):
        raise Exception("'vk.app_secret' configuration option should be defined.")

    # Register resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Register Content Export driver
    content_export.register_driver(ContentExportDriver())

    # Event handlers
    events.listen('pytsite.odm.entity.pre_save.content_export', _eh.odm_entity_pre_save_content_export)

__init()
