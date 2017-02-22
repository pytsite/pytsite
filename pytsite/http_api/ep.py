"""PytSite HTTP API Endpoints
"""
from pytsite import router as _router, http as _http, logger as _logger, lang as _lang, events as _events
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entry(args: dict, inp: dict):
    version = args.pop('version')
    endpoint = '/' + args.pop('endpoint')  # type: str
    current_path = _router.current_path(resolve_alias=False, strip_lang=False)

    # Switch language
    language = _router.request().headers.get('PytSite-Lang')
    if language and _lang.is_defined(language):
        _lang.set_current(language)

    try:
        _events.fire('pytsite.http_api.pre_request')

        rule = _api.match(_router.request().method, endpoint, int(version))

        _events.fire('pytsite.http_api.request')

        status = 200
        r = rule.handler(_router.request().inp, **rule.args)
        if isinstance(r, tuple):
            if len(r) > 1:
                body, status = r[0], r[1]
            else:
                body = r[0]
        else:
            body = r

        # Simple string should be returned as text/html
        if isinstance(body, str):
            response = _http.response.Response(body, status, mimetype='text/html')
        else:
            response = _http.response.JSON(body, status)

        response.headers.add('PytSite-HTTP-API', version)

        return response

    except _http.error.Base as e:
        _logger.error('{} {}: {}'.format(_router.request().method, current_path, e.description))
        response = _http.response.JSON({'error': e.description}, e.code)
        response.headers.add('PytSite-HTTP-API', version)

        return response

    except Exception as e:
        _logger.error(current_path + ': ' + str(e), exc_info=e)
        response = _http.response.JSON({'error': str(e)}, 500)
        response.headers.add('PytSite-HTTP-API', version)

        return response
