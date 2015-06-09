"""Content Plugin endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import reg, router
from pytsite.core.http.errors import NotFoundError
from pytsite.content import content_manager


def view(args: dict, inp: dict):
    """View entity.
    """
    model = args.get('model')
    eid = args.get('eid')

    entity = content_manager.find(model).where('_id', '=', eid)
    if not entity:
        raise NotFoundError()

    endpoint = reg.get('content.endpoints.view.' + model, 'app.endpoints.' + model + '_view')

    return router.call_endpoint(endpoint, {'entity': entity})
