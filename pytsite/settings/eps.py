"""Settings Plugin Endpoints
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from pytsite.core import tpl as _tpl, metatag as _metatag, lang as _lang, router as _router, http as _http
from . import _functions

def form(args: dict, inp: dict) -> str:
    """Render settings form.
    """
    uid = args.get('uid')
    setting_def = _functions.get_definition(uid)
    _metatag.t_set('title', _lang.t(setting_def['title']))

    frm = _functions.get_form(uid)

    for k, v in _functions.get_setting(uid).items():
        field_name = 'setting_' + k
        if frm.has_widget(field_name):
            frm.get_widget(field_name).set_value(v)

    return _tpl.render('settings@form', {'form': frm})


def form_validate(args: dict, inp: dict) -> dict:
    """Validate entity create/modify form.
    """
    global_messages = []
    uid = inp.get('__setting_uid')
    frm = _functions.get_form(uid)
    v_status = frm.fill(inp, validation_mode=True).validate()
    widget_messages = frm.messages

    return {'status': v_status, 'messages': {'global': global_messages, 'widgets': widget_messages}}

def form_submit(args: dict, inp: dict) -> _http.response.RedirectResponse:
    """Process settings form submit.
    """
    uid = args.get('uid')
    frm = _functions.get_form(uid).fill(inp)

    value = {}
    for k, v in frm.values.items():
        if k.startswith('setting_'):
            k = _re.sub('^setting_', '', k)
            value[k] = v

    _functions.set_setting(uid, value)
    _router.session.add_success(_lang.t('settings@settings_has_been_saved'))

    return _http.response.RedirectResponse(frm.values['__form_location'])
