"""PytSite VK Package.
"""
from ._session import Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import content_export, assetman, lang, events, settings, permissions
    from . import _eh, _settings_form
    from ._content_export import Driver as ContentExportDriver

    # Register resources
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # Register Content Export driver
    content_export.register_driver(ContentExportDriver())

    # Register settings form
    permissions.define_permission('vk.settings.manage', 'pytsite.vk@manage_vk_settings', 'app')
    settings.define('vk', _settings_form.Form, 'pytsite.vk@vkontakte', 'fa fa-vk', 'vk.settings.manage')

    # Event handlers
    events.listen('pytsite.odm.entity.pre_save.content_export', _eh.odm_entity_pre_save_content_export)


__init()
