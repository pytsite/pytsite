"""PytSite Form AJAX Endpoints.
"""
from pytsite import util as _util
from . import _error, _form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _create_form(inp: dict, fill_mode: str = None) -> _form.Form:
    """Create and fill form based on the request input.
    """
    args = {}
    for k, v in inp.items():
        # Extract all input start from '__form_data_' to args variable
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
        raise ValueError('Form CID is not specified. Arguments was: {}'.format(args))
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

    # Filter out non-widget (form-related) data
    values = {}
    for k, v in inp.items():
        if not k.startswith('__form_data_'):
            values[k] = v

    return frm.fill(values, mode=fill_mode)


def post_widgets(**kwargs) -> dict:
    """Get widgets of the form for particular step.

    We use POST method here due to large request size in some cases.
    """
    frm = _create_form(kwargs)

    r = []
    for widget in frm.get_widgets(step=frm.step, recursive=True).values():
        # Return widgets as flat list, without rendering children of containers,
        # due to requirements of JavaScript code on client side.
        r.append(widget.render(skip_children=True))

    return r


def post_validate(**kwargs) -> dict:
    """Default form's AJAX validator.
    """
    try:
        _create_form(kwargs, 'validation').validate()
        return {'status': True}

    except _error.ValidationError as e:
        return {'status': False, 'messages': e.errors}
