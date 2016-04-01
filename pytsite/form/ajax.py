"""PytSite Form AJAX Endpoints.
"""
from pytsite import util as _util, router as _router
from . import _error, _form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _create_form(inp: dict, fill_mode: str = None) -> _form.Form:
    """Create and fill form based on the request input.
    """
    args = {}
    for k, v in inp.items():
        if k.startswith('__form_data_'):
            k = _util.to_snake_case(k.replace('__form_data_', ''))
            if k not in ('get_widgets_ep', 'validation_ep', 'steps'):
                if v == 'None':
                    v = None
                elif v == 'False':
                    v = False
                elif v == 'True':
                    v = True

                args[k] = v

    # Get form class ID
    if 'cid' not in args:
        raise ValueError('Form CID is not specified.')
    cid = args['cid']
    del args['cid']

    # Get form UID
    if 'uid' not in args:
        raise ValueError('Form UID is not specified.')
    uid = args['uid']
    del args['uid']

    # Check form class inheritance
    frm_cls = _util.get_class(cid)
    if not issubclass(frm_cls, _form.Form):
        raise TypeError('Invalid form class ID: ' + inp['__form_cid'])

    # Create form
    frm = frm_cls(uid, **args)  # type: _form.Form

    # Filter out non-widget data
    values = {}
    for k, v in inp.items():
        if not k.startswith('__form_data_'):
            values[k] = v

    return frm.fill(values, mode=fill_mode)


def get_widgets(args: dict, inp: dict) -> dict:
    r = []
    for widget in _create_form(inp).get_widgets(step=int(inp.get('__form_step', 1))).values():
        r.append({
            'uid': widget.uid,
            'weight': widget.weight,
            'formArea': widget.form_area,
            'formStep': widget.form_step,
            'assets': widget.assets,
            'content': widget.render(),
        })

    _router.set_no_cache(True)

    return r


def validate(args: dict, inp: dict) -> dict:
    """Default form AJAX validator.
    """
    try:
        _create_form(inp, 'validation').validate()
        return {'status': True}

    except _error.ValidationError as e:
        return {'status': False, 'messages': e.errors}
