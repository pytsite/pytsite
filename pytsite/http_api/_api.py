"""PytSite HTTP API Functions.
"""
from typing import Tuple as _Tuple
from importlib import import_module as _import_module
from pytsite import router as _router, reg as _reg, util as _util
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_package_aliases = {}


def _get_endpoint_struct(endpoint: str) -> _Tuple[str, str]:
    """Convert endpoint string representation into a tuple.
    """
    ep_split = endpoint.split('/')
    package = 'app'

    if len(ep_split) > 1:
        package = '.'.join(ep_split[:-1])
        callback = ep_split[-1]
    else:
        callback = ep_split[0]

    if package in _package_aliases:
        package = _package_aliases[package]

    if package.startswith('app') and len(package) > 3:
        p_split = package.split('.')
        package = p_split[0] + '.http_api.' + '.'.join(p_split[1:])
    else:
        package += '.http_api'

    return package, callback


def url(endpoint: str, version: int = None, **kwargs):
    """Generate URL for an HTTP API endpoint.
    """
    kwargs.update({
        'version': version or _reg.get('http_api.version', 1),
        'endpoint': endpoint,
    })

    return _router.ep_url('pytsite.http_api@entry', kwargs)


def call_ep(endpoint: str, method: str, inp: dict, version: int = None) -> tuple:
    """Call an HTTP endpoint.
    """
    method = method.lower()

    if version is None:
        version = _reg.get('http_api.version', 1)

    package, callback = _get_endpoint_struct(endpoint)

    callback_obj = None

    # Searching for callable endpoint
    for v in ('v' + str(version) + '_', ''):
        try:
            callback_obj = _util.get_callable('{}.{}{}_{}'.format(package, v, method, callback))
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


def register_package_alias(alias: str, package: str):
    """Register an alias name for package.
    """
    if alias in _package_aliases:
        raise RuntimeError("Alias '{}' is already registered.".format(alias))

    try:
        _import_module(package)
    except ImportError:
        raise RuntimeError("Package '{}' does not exist.".format(package))

    _package_aliases[alias] = package
