"""Settings Plugin Endpoints
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from pytsite import auth as _auth, tpl as _tpl, metatag as _metatag, lang as _lang, router as _router, http as _http, \
    validation as _validation
from . import _functions


def form(args: dict, inp: dict) -> str:
    """Render settings form.
    """
    uid = args.get('uid')

    if not _check_permissions(uid):
        raise _http.error.Forbidden()

    setting_def = _functions.get_definition(uid)
    _metatag.t_set('title', _lang.t(setting_def['title']))

    frm = _functions.get_form(uid)

    for k, v in _functions.get_setting(uid).items():
        field_name = 'setting_' + k
        if frm.has_widget(field_name):
            frm.get_widget(field_name).set_value(v)

    return _tpl.render('pytsite.settings@form', {'form': frm})


def form_validate(args: dict, inp: dict) -> dict:
    """Validate entity create/modify form.
    """
    uid = inp.get('__setting_uid')

    if not _check_permissions(uid):
        raise _http.error.Forbidden()


    try:
        _functions.get_form(uid).fill(inp, validation_mode=True).validate()
        return {'status': True}
    except _validation.error.ValidatorError as e:
        return {'status': False, 'messages': {'widgets': e.errors}}


def form_submit(args: dict, inp: dict) -> _http.response.Redirect:
    """Process settings form submit.
    """
    uid = args.get('uid')
    if not _check_permissions(uid):
        raise _http.error.Forbidden()

    frm = _functions.get_form(uid).fill(inp)

    value = {}
    for k, v in frm.values.items():
        if k.startswith('setting_'):
            k = _re.sub('^setting_', '', k)
            value[k] = v

    _functions.set_setting(uid, value)
    _router.session.add_success(_lang.t('pytsite.settings@settings_has_been_saved'))

    return _http.response.Redirect(frm.values['__form_location'])


def _check_permissions(uid: str) -> bool:
    section_def = _functions.get_definition(uid)
    if section_def['perm_name'] == '*':
        return True

    return _auth.get_current_user().has_permission(section_def['perm_name'])
