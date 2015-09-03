"""Auth Log Package Init.
"""
from pytsite import events as _events, odm as _odm
from . import _eh, _odm_model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_odm.register_model('auth_log', _odm_model.AuthLog)
_events.listen('pytsite.auth.login', _eh.auth_login)
_events.listen('pytsite.auth.logout', _eh.auth_logout)
