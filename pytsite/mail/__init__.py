"""Pytsite Mail Subsystem.
"""
# Public API
from ._api import mail_from
from ._message import Message

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, router, settings, permissions
    from . import _settings_form

    lang.register_package(__name__)

    permissions.define_permission('mail.settings.manage', 'pytsite.mail@manage_mail_settings', 'app')
    settings.define('mail', _settings_form.Form, 'pytsite.mail@mail', 'fa fa-envelope', 'mail.settings.manage')

    if not settings.get('mail.from'):
        settings.put('mail.from', 'info@' + router.server_name())


_init()
