"""PytSite HTTP API Endpoints.
"""
from pytsite import router as _router, http as _http, logger as _logger, lang as _lang
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entry(args: dict, inp: dict):
    version = args.pop('version')
    endpoint = args.pop('endpoint')  # type: str
    method = _router.request().method.lower()

    try:
        if 'language' in inp:
            _lang.set_current(inp['language'])

        status, body = _api.call_ep(endpoint, method, inp, version)

        # Simple string should be returned as text/html
        if isinstance(body, str):
            response = _http.response.Response(body, status, mimetype='text/html')
        else:
            response = _http.response.JSON(body, status)

        response.headers.add('PytSite-HTTP-API', version)

        return response

    except _error.EndpointNotFound as e:
        _logger.warn(_router.current_path() + ': ' + str(e))
        response = _http.response.JSON({'error': str(e)}, 404)
        response.headers.add('PytSite-HTTP-API', version)
        return response

    except _http.error.Base as e:
        _logger.error(_router.current_path() + ': ' + str(e.description))
        response = _http.response.JSON({'error': str(e.description)}, e.code)
        response.headers.add('PytSite-HTTP-API', version)
        return response

    except Exception as e:
        _logger.error(_router.current_path() + ': ' + str(e), exc_info=e)
        response = _http.response.JSON({'error': str(e)}, 500)
        response.headers.add('PytSite-HTTP-API', version)
        return response
