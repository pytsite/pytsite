"""PytSite AJAX Endpoints.
"""
from pytsite import http as _http, reg as _reg, logger as _logger, util as _util
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entry(args: dict, inp: dict) -> _http.response.JSON:
    """AJAX endpoint proxy.
    """
    theme = _reg.get('output.theme')
    ep_name = str(args.get('endpoint')).replace('$theme', 'app.themes.' + theme).replace('@', '.js_api.')

    try:
        r = _util.get_callable(ep_name)(inp)

        return r if isinstance(r, _http.response.JSON) else _http.response.JSON(r)

    except ImportError as e:
        _logger.warn("Endpoint '" + ep_name + '": ' + str(e))
        raise _http.error.NotFound()

    except _http.error.Base as e:
        _logger.warn("Endpoint '" + ep_name + '": ' + str(e))
        return _http.response.JSON({'error': e.description}, status=e.code)

    except Exception as e:
        _logger.error("Endpoint '" + ep_name + '": ' + str(e), exc_info=e, stack_info=True)
        return _http.response.JSON({'error': str(e)}, status=500)
