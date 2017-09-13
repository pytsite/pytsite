"""PytSite Form API
"""
from pytsite import util as _util
from . import _form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def dispense(request_inp: dict, fill_mode: str = None) -> _form.Form:
    """Create and fill form based on the request input.
    """
    kwargs = {}
    values = {}

    # Filter out non-widget (form-related) data
    for k, v in request_inp.items():
        if k.startswith('__form_data_'):
            kwargs[k.replace('__form_data_', '')] = v
        else:
            values[k] = v

    form_cid = kwargs.get('cid')
    if not form_cid:
        raise RuntimeError('Form CID is not specified')
    frm = _util.get_module_attr(form_cid)(**kwargs)

    # Setup widgets
    frm.step = int(kwargs.get('step', 1))
    frm.setup_widgets()

    return frm.fill(values, mode=fill_mode)
