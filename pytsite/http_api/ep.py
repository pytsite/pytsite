"""PytSite HTTP API Endpoints
"""
from pytsite import router as _router, http as _http, logger as _logger, lang as _lang, events as _events, \
    util as _util, theme as _theme
from . import _api, _controller

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def entry(version: str, endpoint: str):
    version = int(version)
    endpoint = '/' + endpoint
    current_path = _router.current_path(resolve_alias=False, strip_lang=False)
    request_method = _router.request().method

    # Switch language
    language = _router.request().headers.get('PytSite-Lang')
    if language and _lang.is_defined(language):
        _lang.set_current(language)

    try:
        _events.fire('pytsite.http_api.pre_request')

        rule = _api.match(_router.request().method, endpoint, version)

        _events.fire('pytsite.http_api.request')

        handler = rule.handler
        if isinstance(handler, str):
            handler = handler.replace('$theme', _theme.get().name)
            handler = handler.replace('@', '.http_api_ep.')
            handler = _util.get_callable(handler)

        status = 200
        if issubclass(handler, _controller.Controller):
            controller = handler()  # type: _controller.Controller
            controller.args = rule.args
            controller.inp = _router.request().inp
            handler_response = controller.exec()
        else:
            handler_response = handler(_router.request().inp, **rule.args)

        if isinstance(handler_response, tuple):
            if len(handler_response) > 1:
                body, status = handler_response[0], handler_response[1]
            else:
                body = handler_response[0]
        else:
            body = handler_response

        # Simple string should be returned as text/html
        if isinstance(body, str):
            response = _http.response.Response(body, status, mimetype='text/html')
        else:
            response = _http.response.JSON(body, status)

        response.headers.add('PytSite-HTTP-API', version)

        return response

    except _http.error.Base as e:
        _logger.error('{} {}: {}'.format(request_method, current_path, e.description))
        response = _http.response.JSON({'error': e.description}, e.code)
        response.headers.add('PytSite-HTTP-API', version)

        return response

    except Exception as e:
        _logger.error('{} {}: {}'.format(request_method, current_path, e), exc_info=e)
        response = _http.response.JSON({'error': str(e)}, 500)
        response.headers.add('PytSite-HTTP-API', version)

        return response
