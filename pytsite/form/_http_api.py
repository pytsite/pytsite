"""PytSite Form AJAX Endpoints.
"""
from . import _error, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_widgets(inp: dict, uid: str) -> dict:
    """Get widgets of the form for particular step.

    We use POST method here due to large request size in some cases.
    """
    inp['__form_data_uid'] = uid

    frm = _api.dispense(inp)

    r = []
    for w in frm.get_widgets():
        # Return only top widgets, because they render their children's HTML code by themselves
        if not w.parent:
            r.append(w.render())

    return r


def post_validate(inp: dict, uid: str) -> dict:
    """Default form's AJAX validator.
    """
    try:
        inp['__form_data_uid'] = uid
        _api.dispense(inp, 'validation').validate()
        return {'status': True}

    except _error.ValidationError as e:
        return {'status': False, 'messages': e.errors}
