"""PytSite Form AJAX Endpoints.
"""
from . import _error, _form, _cache

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _dispense_form(uid:str, inp: dict, fill_mode: str = None) -> _form.Form:
    """Create and fill form based on the request input.
    """
    # Get form from the cache
    frm = _cache.get(uid)

    # Filter out non-widget (form-related) data
    values = {}
    for k, v in inp.items():
        if not k.startswith('__form_data_'):
            values[k] = v

    # Setup widgets
    frm.step = int(inp.get('__form_data_step', 1))
    frm.setup_widgets()

    return frm.fill(values, mode=fill_mode)


def get_widgets(inp: dict, uid: str) -> dict:
    """Get widgets of the form for particular step.

    We use POST method here due to large request size in some cases.
    """
    frm = _dispense_form(uid, inp)

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
        _dispense_form(uid, inp, 'validation').validate()
        return {'status': True}

    except _error.ValidationError as e:
        return {'status': False, 'messages': e.errors}
