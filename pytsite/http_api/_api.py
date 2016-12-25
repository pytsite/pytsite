"""PytSite HTTP API Functions.
"""
from importlib import import_module as _import_module
from pytsite import router as _router, util as _util
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_handlers = {}


def register_handler(prefix: str, module):
    """Register API requests handler.
    """
    if prefix in _handlers:
        raise RuntimeError("HTTP API endpoint '{}' is already registered with module '{}'."
                           .format(prefix, _handlers[prefix]))

    try:
        if isinstance(module, str):
            module = _import_module(module)
    except ImportError:
        raise RuntimeError("Module '{}' is not found.".format(module))

    _handlers[prefix] = module


def url(endpoint: str, version: int = 1, **kwargs):
    """Generate URL for an HTTP API endpoint.
    """
    kwargs.update({
        'version': version,
        'endpoint': endpoint,
    })

    return _router.ep_url('pytsite.http_api@entry', kwargs)


def call_endpoint(endpoint: str, method: str, version: int = 1, **kwargs) -> tuple:
    """Call an HTTP endpoint.
    """
    method = method.lower()

    callback_obj = None
    ep_split = endpoint.split('/')

    if len(ep_split) > 1:
        prefix = '/'.join(ep_split[:-1])
        callback_name = ep_split[-1]
    else:
        raise _error.EndpointNotFound('Endpoint not found: {}'.format(endpoint))

    if prefix not in _handlers:
        raise _error.EndpointNotFound('Endpoint not found: {}'.format(endpoint))

    module = _handlers[prefix]

    # Searching for callable in module.
    # First, try '{module}.{method}_{func}', i. e. 'app.get_hello_world()'.
    # Second, try '{module}.v{N}_{method}_{func}', i. e. 'app.v1_get_hello_world()'.
    for v in ('', 'v' + str(version) + '_'):
        try:
            callback_obj = _util.get_callable('{}{}_{}'.format(v, method, callback_name), module)
            break
        except ImportError:
            pass

    if callback_obj is None:
        raise _error.EndpointNotFound('Endpoint not found: {}'.format(endpoint))

    status = 200  # HTTP status by default
    body = callback_obj(**kwargs)
    if isinstance(body, tuple):
        status = body[0]
        body = body[1]

    return status, body


def get(endpoint: str, version: int = 1, **kwargs) -> tuple:
    """Shortcut.
    """
    return call_endpoint(endpoint, 'get', version, **kwargs)


def post(endpoint: str, version: int = 1, **kwargs) -> tuple:
    """Shortcut.
    """
    return call_endpoint(endpoint, 'post',  version, **kwargs)


def patch(endpoint: str, version: int = 1, **kwargs) -> tuple:
    """Shortcut.
    """
    return call_endpoint(endpoint, 'patch',  version, **kwargs)


def delete(endpoint: str, version: int = 1, **kwargs) -> tuple:
    """Shortcut.
    """
    return call_endpoint(endpoint, 'delete',  version, **kwargs)
