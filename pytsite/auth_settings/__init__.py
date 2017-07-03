"""PytSite Auth Settings
"""
from pytsite import lang as _lang, settings as _settings
from . import _settings_form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_lang.register_package(__name__)
_settings.define('auth', _settings_form.Form, 'pytsite.auth_settings@security', 'fa fa-user')
