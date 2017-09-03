"""PytSite HTTP API Endpoints
"""
from pytsite import router as _router, logger as _logger, lang as _lang, events as _events, routing as _routing, \
    http as _http, formatters as _formatters, errors as _errors, reg as _reg
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Entry(_routing.Controller):
    def __init__(self):
        super().__init__()

        self.args.add_formatter('http_api_version', _formatters.Int())

    def exec(self):
        version = self.args.pop('http_api_version')
        endpoint = '/' + self.args.pop('http_api_endpoint')
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

            status = 200
            rule.controller.args.clear().update(self.args).update(rule.args)
            rule.controller.files = self.files
            controller_response = rule.controller.exec()

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
                if isinstance(body, _routing.ControllerArgs):
                    body = dict(body)

                response = _http.response.JSON(body, status)

            response.headers.add('PytSite-HTTP-API', version)

            return response

        except _errors.ForbidOperation as e:
            raise _http.error.Forbidden(e)

        except _http.error.Base as e:
            log_msg = '{} {}: {}'.format(request_method, current_path, e.description)

            if _reg.get('debug'):
                _logger.error(log_msg, exc_info=e)
            else:
                _logger.error(log_msg)

            if e.response and isinstance(e.response, _http.response.JSON):
                response = e.response
                response.status_code = e.code
            else:
                response = _http.response.JSON({'error': e.description}, e.code)

            response.headers.add('PytSite-HTTP-API', version)

            return response

        except Exception as e:
            _logger.error('{} {}: {}'.format(request_method, current_path, e), exc_info=e)
            response = _http.response.JSON({'error': str(e)}, 500)
            response.headers.add('PytSite-HTTP-API', version)

            return response
