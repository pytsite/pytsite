"""PytSite HTTP API Endpoints.
"""
from pytsite import router as _router, http as _http, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entry(args: dict, inp: dict):
    version = args.pop('version')
    package = args.pop('package')
    callback = args.pop('callback')
    method = _router.request().method.lower()

    endpoint = None

    # Searching for callable endpoint
    for v in ('v' + str(version), 'any'):
        possible_ep = '{}.http_api.{}_{}_{}'.format(package, v, method, callback)
        if _router.is_ep_callable(possible_ep):
            endpoint = possible_ep
            break

    try:
        if not endpoint:
            raise _http.error.NotFound('Endpoint not found.')

        code = 200
        r = _router.call_ep(endpoint, None, inp)
        if isinstance(r, dict) and 'code' in r and 'response' in r:
            code = r['code']
            r = r['response']

        return _http.response.JSON(r, code)

    except _http.error.Base as e:
        _logger.warn("Endpoint '" + endpoint + '": ' + str(e), __name__)
        return _http.response.JSON({'error': str(e.description)}, e.code)

    except Exception as e:
        _logger.error("Endpoint '" + endpoint + '": ' + str(e), __name__)
        return _http.response.JSON({'error': str(e)}, 500)
