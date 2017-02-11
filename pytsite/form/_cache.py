"""PytSite Forms Cache.
"""
from datetime import datetime as _datetime
from pytsite import reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_TTL = _reg.get('form.cache.ttl', 21600)
_forms = {}


def put(frm):
    """
    :type frm: pytsite.form.Form
    :rtype: pytsite.form.Form
    """
    if frm.uid in _forms:
        raise RuntimeError("Form '{}' is already cached".format(frm.uid))

    _forms[frm.uid] = frm

    return frm


def get(form_uid: str):
    """
    :rtype: pytsite.form.Form
    """
    try:
        return _forms[form_uid]
    except KeyError:
        raise KeyError("Form UID '{}' is invalid".format(form_uid))


def rm(form_uid: str):
    try:
        del _forms[form_uid]
    except KeyError:
        raise KeyError("Form UID '{}' is invalid".format(form_uid))


def cleanup():
    uids_to_rm = []

    for frm in _forms.values():
        if (_datetime.now() - frm.created).seconds > _TTL:
            uids_to_rm.append(frm.uid)

    for uid in uids_to_rm:
        rm(uid)


def get_size() -> int:
    return len(_forms)
