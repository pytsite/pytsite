"""Content Plugin endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import core as _core, content as _content

def view(args: dict, inp: dict):
    """View entity.
    """
    model = args.get('model')
    eid = args.get('eid')

    entity = _content.manager.find(model).where('_id', '=', eid)
    if not entity:
        raise _core.http.error.NotFoundError()

    endpoint = _core.reg.get('content.endpoints.view.' + model, 'app.endpoints.' + model + '_view')

    return _core.router.call_endpoint(endpoint, {'entity': entity})
