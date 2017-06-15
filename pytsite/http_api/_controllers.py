"""PytSite HTTP API Endpoints
"""
from pytsite import router as _router, logger as _logger, lang as _lang, events as _events, routing as _routing, \
    http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Entry(_routing.Controller):
    def exec(self):
        version = int(self.arg('version'))
        endpoint = '/' + self.arg('endpoint')
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

            controller = rule.controller

            status = 200

            controller.args = _router.request().inp.copy()
            controller.args.update(rule.args)
            controller_response = controller.exec()

            if isinstance(controller_response, tuple):
                if len(controller_response) > 1:
                    body, status = controller_response[0], controller_response[1]
                else:
                    body = controller_response[0]
            else:
                body = controller_response

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
