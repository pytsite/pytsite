"""PytSite HTTP API Functions.
"""
from pytsite import router as _router, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def url(endpoint: str, version: int = None, **kwargs):
    """Generate URL for HTTP API endpoint.
    """
    package = 'app'
    if '@' in endpoint:
        package, callback = endpoint.split('@')[0:2]
    else:
        callback = endpoint

    if version is None:
        version = _reg.get('http_api.version', 1)

    kwargs.update({
        'version': version,
        'package': package,
        'callback': callback,
    })

    return _router.ep_url('pytsite.http_api@entry', kwargs)
