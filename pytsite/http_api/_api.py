"""PytSite HTTP API Functions.
"""
from pytsite import router as _router, reg as _reg, util as _util
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _get_endpoint_struct(endpoint: str) -> tuple:
    package = 'app'
    if '@' in endpoint:
        package, callback = endpoint.split('@')[0:2]
    else:
        callback = endpoint

    return package, callback


def url(endpoint: str, version: int = None, **kwargs):
    """Generate URL for HTTP API endpoint.
    """
    if version is None:
        version = _reg.get('http_api.version', 1)

    package, callback = _get_endpoint_struct(endpoint)

    kwargs.update({
        'version': version,
        'package': package,
        'callback': callback,
    })

    return _router.ep_url('pytsite.http_api@entry', kwargs)


def call_ep(endpoint: str, method: str, inp: dict, version: int = None) -> tuple:
    method = method.lower()

    if version is None:
        version = _reg.get('http_api.version', 1)

    package, callback = _get_endpoint_struct(endpoint)

    callback_obj = None

    # Searching for callable endpoint
    for v in ('v' + str(version) + '_', ''):
        try:
            callback_obj = _util.get_callable('{}.http_api.{}{}_{}'.format(package, v, method, callback))
            break
        except ImportError:
            pass

    if callback_obj is None:
        raise _error.EndpointNotFound('Endpoint not found.')

    status = 200
    body = callback_obj(inp)
    if isinstance(body, tuple):
        status = body[0]
        body = body[1]

    return status, body
