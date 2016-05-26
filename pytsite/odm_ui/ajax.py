"""PytSite ODM AJAX Endpoints.
"""
from pytsite import odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entities_delete(args: dict, inp: dict) -> dict:
    model = inp.get('model')
    ids = inp.get('ids', ())

    if isinstance(ids, str):
        ids = [ids]

    # Delete entities
    for eid in ids:
        entity = _api.dispense_entity(model, eid)

        if not entity.ui_can_be_deleted():
            raise _odm.error.ForbidEntityDelete()

        entity.delete()

    return {'status': True}
