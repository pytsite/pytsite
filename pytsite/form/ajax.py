"""PytSite Form AJAX Endpoints.
"""
from pytsite import util as _util
from . import _error, _form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _create_form(inp: dict) -> _form.Form:
    if '__form_cid' not in inp:
        raise ValueError('Form CID is not specified.')

    frm_cls = _util.get_class(inp['__form_cid'])
    if not issubclass(frm_cls, _form.Form):
        raise TypeError('Invalid form CID: ' + inp['__form_cid'])

    frm = frm_cls()  # type: _form.Form

    values = {}
    for k, v in inp.items():
        if not k.startswith('__'):
            values[k] = v

    return frm.fill(values)


def get_widgets(args: dict, inp: dict) -> dict:
    frm = _create_form(inp)

    r = []

    for widget in frm.get_widgets(step=int(inp.get('__form_step', 1))).values():
        r.append({
            'uid': widget.uid,
            'weight': widget.weight,
            'formArea': widget.form_area,
            'formStep': widget.form_step,
            'cssFiles': widget.css_files,
            'jsFiles': widget.js_files,
            'htmlStr': widget.render(),
        })

    return r


def validate(args: dict, inp: dict) -> dict:
    """Default form AJAX validator.
    """
    try:
        _create_form(inp).validate()
        return {'status': True}

    except _error.ValidationError as e:
        return {'status': False, 'messages': e.errors}
