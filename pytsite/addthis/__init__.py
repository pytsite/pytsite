"""AddThis Plugin Init.
"""
# Public API
from . import _widget as widget


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import lang, tpl, permissions, settings
    from . import _settings_form

    lang.register_package(__name__)
    tpl.register_package(__name__)

    permissions.define_permission('addthis.settings.manage', 'pytsite.addthis@manage_addthis_settings', 'app')
    settings.define('addthis', _settings_form.Form, 'pytsite.addthis@addthis', 'fa fa-plus-square',
                    'addthis.settings.manage')

__init()
