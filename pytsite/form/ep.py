"""PytSite Form Endpoints.
"""
from pytsite import util as _util, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def validate(args: dict, inp: dict) -> dict:
    """Validate a form.
    """
    cid = inp.get('__form_cid')
    if not cid:
        raise ValueError('Form CID is not specified.')

    try:
        _util.get_class(cid)().fill(inp, validation_mode=True).validate()
        return {'status': True}
    except _validation.error.ValidatorError as e:
        return {'status': False, 'messages': {'widgets': e.errors}}
