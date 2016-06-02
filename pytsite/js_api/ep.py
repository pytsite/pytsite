"""PytSite AJAX Endpoints.
"""
from pytsite import http as _http, router as _router, logger as _logger, reg as _reg
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entry(args: dict, inp: dict) -> _http.response.JSON:
    """AJAX endpoint proxy.
    """
    ep_name_split = args.get('endpoint').split('.')
    ep_name = '.'.join(ep_name_split[:-1]) + '.js_api.' + ep_name_split[-1]

    try:
        if not _router.is_ep_callable(ep_name):
            raise _http.error.NotFound()

        r = _router.call_ep(ep_name, None, inp)

        return r if isinstance(r, _http.response.JSON) else _http.response.JSON(r)

    except _http.error.Base as e:
        _logger.warn("Endpoint '" + ep_name + '": ' + str(e), __name__)
        return _http.response.JSON({'error': e.description}, status=e.code)

    except Exception as e:
        _logger.error("Endpoint '" + ep_name + '": ' + str(e), __name__)
        return _http.response.JSON({'error': str(e)}, status=500)
