"""Settings Plugin Endpoints
"""
from pytsite import auth as _auth, metatag as _metatag, lang as _lang, http as _http, admin as _admin
from . import _api, _frm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def form(uid: str) -> str:
    """Render settings form.
    """
    user = _auth.get_current_user()
    setting_def = _api.get_definition(uid)

    if setting_def['perm_name'] != '*' and not user.has_permission(setting_def['perm_name']):
        raise _http.error.Forbidden()

    # Load setting definition
    setting_def = _api.get_definition(uid)

    # Update page's title
    _metatag.t_set('title', _lang.t(setting_def['title']))

    # Instantiate form
    frm = setting_def['form'](setting_uid=uid)  # type: _frm.Form

    return _admin.render_form(frm)
