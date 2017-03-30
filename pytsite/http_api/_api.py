"""PytSite HTTP API Functions
"""
from pytsite import router as _router, http as _http, routing as _routing, logger as _logger, events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_rules_map = _routing.RulesMap()


def handle(method: str, path: str, handler: callable, name: str = None, version: int = 0):
    """Register API requests handler
    """
    _rules_map.add(_routing.Rule(path, handler, name, methods=method, attrs={'version': version}))


def match(method: str, path: str, version: int) -> _routing.Rule:
    try:
        rule = _rules_map.match(path, method)
        if rule.attrs['version'] != 0 and rule.attrs['version'] != version:
            raise _http.error.NotFound()

        return rule

    except _routing.error.RuleNotFound as e:
        _logger.error(e)
        raise _http.error.NotFound()


def url(name: str, args: dict = None, version: int = 1):
    """Generate URL for an HTTP API endpoint.
    """
    return _router.ep_url('pytsite.http_api@entry', {'version': version, 'endpoint': _rules_map.path(name, args)})


def call(name: str, inp: dict = None, **args) -> tuple:
    """Call an HTTP API endpoint.
    """
    return _rules_map.get(name).handler(inp or {}, **args)


def on_pre_request(handler, priority: int = 0):
    """Register handler which will be called before handling every request to HTTP API.
    """
    _events.listen('pytsite.http_api.pre_request', handler, priority)


def on_request(handler, priority: int = 0):
    """Register handler which will be called on every request to HTTP API.
    """
    _events.listen('pytsite.http_api.request', handler, priority)
