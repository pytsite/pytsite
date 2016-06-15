"""PytSite ODM AJAX Endpoints.
"""
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# def entities_delete(inp: dict) -> dict:
#     model = inp.get('model')
#     ids = inp.get('ids', ())
#
#     if isinstance(ids, str):
#         ids = [ids]
#
#     # Delete entities
#     for eid in ids:
#         _api.dispense(model, eid).delete()
#
#     return {'status': True}
