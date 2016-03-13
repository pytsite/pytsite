"""PytSite AJAX Endpoints.
"""
from pytsite import http as _http, router as _router, logger as _logger
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def request(args: dict, inp: dict) -> _http.response.JSON:
    """AJAX endpoint proxy.
    """
    ep_name = args.get('ep')

    try:
        if not _api.is_ep_registered(ep_name):
            raise _http.error.NotFound()

        r = _router.call_ep(ep_name, args, inp)

        return r if isinstance(r, _http.response.JSON) else _http.response.JSON(r)

    except _http.error.NotFound:
        return _http.response.JSON({'error': "Unknown endpoint: '{}'".format(ep_name)}, status=404)

    except Exception as e:
        _logger.error(str(e), __name__)
        return _http.response.JSON({'error': str(e)}, status=500)
