"""PytSite Contact Form.
"""
# Public API
from ._form import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, lang, tpl, http_api, permissions, settings
    from . import _settings_form

    # Resources
    assetman.register_package(__name__)
    lang.register_package(__name__)
    tpl.register_package(__name__)

    # HTTP API endpoints
    http_api.register_package('contact_form', 'pytsite.contact_form.http_api')

    # Settings form
    permissions.define_permission('contact_form.settings.manage', 'pytsite.contact_form@manage_contact_form', 'app')
    settings.define('contact_form', _settings_form.Form, 'pytsite.contact_form@contact_form', 'fa fa-paper-plane',
                    'contact_form.settings.manage')

_init()
