"""PytSite HTTP API Endpoints.
"""
from pytsite import router as _router, http as _http, logger as _logger, util as _util, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entry(args: dict, inp: dict):
    version = args.pop('version')
    package = args.pop('package')
    callback = args.pop('callback')
    method = _router.request().method.lower()

    callback_obj = None

    # Searching for callable endpoint
    for v in ('v' + str(version) + '_', ''):
        try:
            callback_obj = _util.get_callable('{}.http_api.{}{}_{}'.format(package, v, method, callback))
            break
        except ImportError:
            pass

    try:
        if callback_obj is None:
            raise _http.error.NotFound('Endpoint not found')

        code = 200
        r = callback_obj(inp)
        if isinstance(r, dict) and 'code' in r and 'response' in r:
            code = r['code']
            r = r['response']

        return _http.response.JSON(r, code)

    except _http.error.Base as e:
        _logger.warn(_router.current_path() + ': ' + str(e.description), __name__)
        return _http.response.JSON({'error': str(e.description)}, e.code)

    except Exception as e:
        _logger.error(_router.current_path() + ': ' + str(e), __name__)
        return _http.response.JSON({'error': str(e)}, 500)
