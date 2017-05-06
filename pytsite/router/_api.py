"""PytSite Router API.
"""
import re as _re
from typing import Dict as _Dict, Union as _Union
from os import path as _path
from traceback import format_exc as _format_exc
from urllib import parse as _urlparse
from werkzeug.exceptions import HTTPException as _HTTPException
from werkzeug.contrib.sessions import FilesystemSessionStore as _FilesystemSessionStore
from pytsite import reg as _reg, logger as _logger, http as _http, util as _util, lang as _lang, tpl as _tpl, \
    threading as _threading, theme as _theme, setup as _setup, events as _events, routing as _routing
from . import _controller

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_LANG_CODE_RE = _re.compile('^/[a-z]{2}(/|$)')

# Routes map
_routes = _routing.RulesMap()

# Route path aliases
_path_aliases = {}

# Session store
_session_store = _FilesystemSessionStore(path=_reg.get('paths.session'), session_class=_http.session.Session)

# Thread safe requests collection
_requests = {}  # type: _Dict[int, _http.request.Request]

# Thread safe sessions collection
_sessions = {}  # type: _Dict[int, _http.session.Session]

# Thread safe 'no-cache' statues collection
_no_cache = {}  # type: _Dict[int, bool]


def get_session_store() -> _FilesystemSessionStore:
    """Get session store.
    """
    return _session_store


def set_request(r: _http.request.Request):
    """Set request for current thread.
    """
    _requests[_threading.get_id()] = r


def request() -> _Union[_http.request.Request, None]:
    """Get request for current thread.
    """
    return _requests.get(_threading.get_id())


def session() -> _http.session.Session:
    """Get session for current thread.
    """
    return _sessions.get(_threading.get_id())


def get_no_cache() -> bool:
    """Get 'no-cache' status belonged to the current thread
    """
    return _no_cache.get(_threading.get_id())


def set_no_cache(status: bool):
    """Set 'no-cache' status belonged to the current thread
    """
    _no_cache[_threading.get_id()] = status


def handle(path: str, handler: _Union[str, _controller.Controller], name: str = None, defaults: dict = None,
           methods='GET', filters=None):
    """Add a rule to the router.
    """
    if not isinstance(handler, str) and not issubclass(handler, _controller.Controller):
        raise RuntimeError('Handler should be a string or a controller class, got {}'.format(type(handler)))

    if isinstance(filters, str):
        filters = (filters,)

    _routes.add(_routing.Rule(path, handler, name, defaults, methods, {'filters': filters or ()}))


def handle_post(path: str, handler: _Union[str, _controller.Controller], name: str = None, defaults: dict = None,
                filters=None):
    """Shortcut.
    """
    handle(path, handler, name, defaults, 'POST', filters)


def add_path_alias(alias: str, target: str):
    """Add an alias for a path.
    """
    _path_aliases[alias] = target


def remove_path_alias(alias: str):
    """Remove an alias for a path.
    """
    if alias in _path_aliases:
        del _path_aliases[alias]


def is_ep_callable(ep_name: str) -> bool:
    """Check whether endpoint is callable.
    """
    try:
        resolve_ep_callable(ep_name)
        return True
    except ImportError:
        return False


def resolve_ep_callable(handler: str) -> callable:
    if '$theme' in handler:
        handler = handler.replace('$theme', _theme.get().name)

    if '@' in handler:
        handler = handler.replace('@', '.ep.')

    return _util.get_callable(handler)


def call_ep(ep_name: str, **kwargs):
    """Call an endpoint.
    """
    return resolve_ep_callable(ep_name)(**kwargs)


def dispatch(env: dict, start_response: callable):
    """Dispatch a request.
    """
    tid = _threading.get_id()

    # Check if the setup completed
    if not _setup.is_setup_completed():
        wsgi_response = _http.response.Response(response='Setup is not completed', status=503, content_type='text/html')
        return wsgi_response(env, start_response)

    # Check maintenance mode status
    if _path.exists(_reg.get('paths.maintenance.lock')):
        wsgi_response = _http.response.Response(response=_lang.t('pytsite.router@we_are_in_maintenance'),
                                                status=503, content_type='text/html')
        return wsgi_response(env, start_response)

    # Creating request context
    req = _http.request.Request(env)
    set_request(req)

    # Remove trailing slash
    if req.path != '/' and req.path.endswith('/'):
        redirect_url = _re.sub('/$', '', req.path)
        redirect_url += '?' + req.query_string.decode('utf-8') if req.query_string else ''
        return _http.response.Redirect(redirect_url, 301)(env, start_response)

    # All requests are cached by default
    set_no_cache(False)

    # Detect language from path
    languages = _lang.langs()
    if len(languages) > 1:
        if _LANG_CODE_RE.search(req.path):
            # Extract language code as first two-letters of the path
            lang_code = req.path[1:3]
            try:
                _lang.set_current(lang_code)
                req.path = req.path[3:]
                if not req.path:
                    req.path = '/'
                # If requested language is default, redirect to path without language prefix
                if lang_code == languages[0]:
                    return _http.response.Redirect(req.path, 301)(env, start_response)
            except _lang.error.LanguageNotSupported:
                # If language is not defined, do nothing. 404 will fired in the code below.
                pass
        else:
            # No language code found in the path. Set first defined language as current.
            _lang.set_current(languages[0])

    # Notify listeners
    if req.is_xhr:
        _events.fire('pytsite.router.xhr_pre_dispatch.{}'.format(req.method.lower()))
    else:
        _events.fire('pytsite.router.pre_dispatch.{}'.format(req.method.lower()))

    # Loading path alias, if it exists or use current one
    if req.path in _path_aliases:
        req.path = _path_aliases[req.path]

    # Shortcuts
    request_input = req.inp
    request_cookies = req.cookies

    # Session setup
    sid = request_cookies.get('PYTSITE_SESSION')
    if sid:
        _sessions[tid] = _session_store.get(sid)
    else:
        _sessions[tid] = _session_store.new()

    # Processing request
    try:
        # Notify listeners
        if req.is_xhr:
            _events.fire('pytsite.router.xhr_dispatch.{}'.format(req.method.lower()))
        else:
            _events.fire('pytsite.router.dispatch.{}'.format(req.method.lower()))

        # Search for rule
        try:
            rule = _routes.match(req.path, req.method)
            rule_handler = rule.handler
            rule_args = rule.args.copy()
            rule_attrs = rule.attrs.copy()

            # Try to find referenced rule by name
            if isinstance(rule_handler, str):
                try:
                    ref_rule = _routes.get(rule_handler)

                    rule_handler = ref_rule.handler

                    ref_rule_args = ref_rule.args.copy()
                    ref_rule_args.update(rule_args)
                    rule_args = ref_rule_args

                    ref_rule_attrs = ref_rule.attrs.copy()
                    ref_rule_attrs.update(rule_attrs)
                    rule_attrs = ref_rule_attrs
                except _routing.error.RuleNotFound:
                    pass
        except _routing.error.RuleNotFound as e:
            raise _http.error.NotFound(e)

        # Processing rule filters
        for flt in rule_attrs['filters']:
            flt_args = rule_args
            flt_split = flt.split(':')
            flt_endpoint = flt_split[0]
            if len(flt_split) > 1:
                for flt_arg_str in flt_split[1:]:
                    flt_arg_str_split = flt_arg_str.split('=')
                    if len(flt_arg_str_split) == 2:
                        flt_args[flt_arg_str_split[0]] = flt_arg_str_split[1]

            flt_response = call_ep(flt_endpoint, **flt_args)
            if isinstance(flt_response, _http.response.Redirect):
                return flt_response(env, start_response)

        # Preparing response object
        wsgi_response = _http.response.Response(response='', status=200, content_type='text/html', headers=[])
        handler_resp = None

        # Resolve handler's callable
        if isinstance(rule_handler, str):
            rule_handler = resolve_ep_callable(rule_handler)

        # Calling the handler
        if issubclass(rule_handler, _controller.Controller):
            # Instantiate controller and fill it with values
            controller = rule_handler()  # type: _controller.Controller
            controller.args = rule_args
            controller.inp = req.inp
            handler_resp = controller.exec()
        elif callable(rule_handler):
            try:
                handler_resp = rule_handler(**rule_args)
            except ImportError as e:
                raise _http.error.NotFound(e)

        # Checking response from the handler
        if isinstance(handler_resp, str):
            # Minifying output
            if _reg.get('output.minify'):
                handler_resp = _util.minify_html(handler_resp)
            wsgi_response.data = handler_resp
        elif isinstance(handler_resp, _http.response.Response):
            wsgi_response = handler_resp
        else:
            wsgi_response.data = ''

        # Cache control
        if get_no_cache() or req.method != 'GET':
            wsgi_response.headers.set('Cache-Control', 'private, max-age=0, no-cache, no-store')
            wsgi_response.headers.set('Pragma', 'no-cache')
        else:
            wsgi_response.headers.set('Cache-Control', 'public')

        # Store updated session data
        if session().should_save:
            _session_store.save(session())
            wsgi_response.set_cookie('PYTSITE_SESSION', session().sid)

        if req.is_xhr:
            _events.fire('pytsite.router.xhr_response.{}'.format(req.method.lower()), response=wsgi_response)
        else:
            _events.fire('pytsite.router.response.{}'.format(req.method.lower()), response=wsgi_response)

        return wsgi_response(env, start_response)

    except Exception as e:
        if isinstance(e, _HTTPException):
            # Exception can contain response object in its body
            if isinstance(e.response, _http.response.Response):
                # For non-redirect embedded responses use original status code from exception
                if not isinstance(e.response, _http.response.Redirect):
                    e.response.status_code = e.code
                return e.response(env, start_response)
            else:
                code = e.code
                title = _lang.t('pytsite.router@http_error_' + str(e.code))
                _logger.error('HTTP {} {} ({}): {}'.format(
                    e.code, e.name, current_path(resolve_alias=False, strip_lang=False), e.description))
        else:
            code = 500
            title = _lang.t('pytsite.router@error', {'code': '500'})
            _logger.error(e, exc_info=e)

        args = {
            'title': title,
            'exception': e,
            'traceback': _format_exc()
        }

        # Notify listeners
        _events.fire('pytsite.router.exception', args=args)

        # User defined exception handler
        if is_ep_callable('$theme@exception'):
            wsgi_response = call_ep('$theme@exception', **args)

        # Builtin exception handler
        else:
            try:
                # User defined template
                wsgi_response = _tpl.render('$theme@exception', args)
            except _tpl.error.TemplateNotFound:
                try:
                    # Default template
                    wsgi_response = _tpl.render('pytsite.router@exception', args)
                except _tpl.error.TemplateNotFound:
                    # Default simple template
                    wsgi_response = _tpl.render('pytsite.router@exception-simple', args)

        return _http.response.Response(wsgi_response, code, content_type='text/html')(env, start_response)


def base_path(lang: str = None) -> str:
    """Get base path of application.
    """
    available_langs = _lang.langs()

    if len(available_langs) == 1:
        return '/'

    lang = lang or _lang.get_current()

    if lang not in available_langs:
        raise RuntimeError("Language '{}' is not supported.".format(lang))

    return '/' if lang == _lang.get_primary() else '/' + lang


def server_name():
    """Get server's name.
    """
    r = request()

    return r.host if r else _reg.get('server_name', 'localhost')


def scheme():
    """Get current URL scheme.
    """
    r = request()

    return r.scheme if (r and r.scheme) else 'http'


def base_url(lang: str = None, query: dict = None):
    """Get base URL of the application.
    """
    r = scheme() + '://' + server_name() + base_path(lang)
    if query:
        r = url(r, query=query)

    return r


def is_base_url(compare: str = None) -> bool:
    """Check if the given URL is base.
    """
    if not compare:
        compare = current_url(True)

    return base_url() == compare


def url(s: str, **kwargs) -> str:
    """Generate an URL.
    """
    if not s:
        raise ValueError('url_str cannot be empty.')

    lang = kwargs.get('lang', _lang.get_current())  # type: str
    strip_lang = kwargs.get('strip_lang', False)  # type: bool
    strip_query = kwargs.get('strip_query')  # type: bool
    query = kwargs.get('query')  # type: dict
    relative = kwargs.get('relative', False)  # type: bool
    strip_fragment = kwargs.get('strip_fragment')  # type: bool
    fragment = kwargs.get('fragment')  # type: str

    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
    parsed_url = _urlparse.urlparse(s)
    r = [
        parsed_url[0] if parsed_url[0] else scheme(),  # 0, Scheme
        parsed_url[1] if parsed_url[1] else server_name(),  # 1, Netloc
        parsed_url[2] if parsed_url[2] else '',  # 2, Path
        parsed_url[3] if parsed_url[3] else '',  # 3, Params
        parsed_url[4] if parsed_url[4] else '',  # 4, Query
        parsed_url[5] if parsed_url[5] else '',  # 5, Fragment
    ]

    if relative:
        r[0] = ''
        r[1] = ''

    if strip_query:
        # Stripping query
        r[4] = ''
    elif query:
        # Attaching additional query arguments
        parsed_qs = _urlparse.parse_qs(parsed_url[4])
        parsed_qs.update(query)
        r[4] = _urlparse.urlencode(parsed_qs, doseq=True)

    if strip_fragment:
        # Stripping fragment
        r[5] = ''
    elif fragment:
        # Attaching additional fragment
        r[5] = fragment

    # Adding language suffix (only for relative links as source argument)
    if not parsed_url[0] and not strip_lang:
        lang_re = '^/({})/'.format('|'.join(_lang.langs()))
        if not _re.search(lang_re, parsed_url[2]):
            b_path = base_path(lang)
            if not b_path.endswith('/') and not parsed_url[2].startswith('/'):
                b_path += '/'
            r[2] = str(b_path + parsed_url[2]).replace('//', '/')

    return _urlparse.urlunparse(r)


def current_path(strip_query=False, resolve_alias=True, strip_lang=True, lang: str = None) -> str:
    """Get current path.
    """
    lang = lang or _lang.get_current()
    req = request()

    r = req.path if req else '/'

    if resolve_alias:
        for alias, target in _path_aliases.items():
            if r == target:
                r = alias
                break

    if not strip_lang and lang != _lang.get_primary():
        r = '/' + lang + (r if r != '/' else '')

    if not strip_query and req and req.query_string:
        r += '?' + req.query_string.decode('utf-8')

    return r


def current_url(strip_query: bool = False, resolve_alias: bool = True, lang: str = None, add_query: dict = None,
                add_fragment: str = None) -> str:
    """Get current URL.
    """
    r = scheme() + '://' + server_name() + current_path(strip_query, resolve_alias, False, lang)
    if add_query or add_fragment:
        r = url(r, query=add_query, fragment=add_fragment)

    return r


def ep_path(ep_name: str, args: dict = None) -> str:
    """Get path for an endpoint.
    """
    return _routes.path(ep_name, args)


def ep_url(ep_name: str, route_args: dict = None, **kwargs) -> str:
    """Get URL for an endpoint.
    """
    return url(ep_path(ep_name, route_args), **kwargs)


def on_pre_dispatch(handler, priority: int = 0, method: str = 'get'):
    _events.listen('pytsite.router.pre_dispatch.{}'.format(method.lower()), handler, priority)


def on_xhr_pre_dispatch(handler, priority: int = 0, method: str = 'get'):
    _events.listen('pytsite.router.xhr_pre_dispatch.{}'.format(method.lower()), handler, priority)


def on_dispatch(handler, priority: int = 0, method: str = 'get'):
    _events.listen('pytsite.router.dispatch.{}'.format(method.lower()), handler, priority)


def on_xhr_dispatch(handler, priority: int = 0, method: str = 'get'):
    _events.listen('pytsite.router.xhr_dispatch.{}'.format(method.lower()), handler, priority)


def on_response(handler, priority: int = 0, method: str = 'get'):
    _events.listen('pytsite.router.response.{}'.format(method.lower()), handler, priority)


def on_xhr_response(handler, priority: int = 0, method: str = 'get'):
    _events.listen('pytsite.router.xhr_response.{}'.format(method.lower()), handler, priority)


def on_exception(handler, priority: int = 0):
    _events.listen('pytsite.router.exception', handler, priority)
