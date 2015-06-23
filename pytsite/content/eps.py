"""Content Plugin endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import content as _content
from pytsite.core import reg as _reg, http as _http, router as _router, metatag as _metatag

def view(args: dict, inp: dict):
    """View entity.
    """
    model = args.get('model')
    entity = _content.manager.find(model).where('_id', '=', args.get('id')).first()
    if not entity:
        raise _http.error.NotFoundError()

    _metatag.t_set('title', entity.f_get('title'))

    endpoint = _reg.get('content.endpoints.view.' + model, 'app.eps.' + model + '_view')

    return _router.call_endpoint(endpoint, {'entity': entity})
