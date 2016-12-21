"""PytSite Router API.
"""
import re as _re
from typing import Dict as _Dict, Union as _Union
from os import path as _path
from traceback import format_exc as _format_exc
from urllib import parse as _urlparse
from werkzeug.routing import Map as _Map, Rule as _Rule, MapAdapter as _MapAdapter
from werkzeug.exceptions import HTTPException as _HTTPException
from werkzeug.contrib.sessions import FilesystemSessionStore as _FilesystemSessionStore
from pytsite import reg as _reg, logger as _logger, http as _http, util as _util, lang as _lang, tpl as _tpl, \
    threading as _threading, theme as _theme, setup as _setup

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Routes map
_routes = _Map()

# Route path aliases
_path_aliases = {}

# Session store
_session_store = _FilesystemSessionStore(path=_reg.get('paths.session'), session_class=_http.session.Session)

# Thread safe map adapters collection
_map_adapters = {}  # type: _Dict[int, _MapAdapter]

# Thread safe requests collection
_requests = {}  # type: _Dict[int, _http.request.Request]

# Thread safe sessions collection
_sessions = {}  # type: _Dict[int, _http.session.Session]

# Thread safe 'no-cache' statues collection
_no_cache = {}  # type: _Dict[int, bool]


class Rule(_Rule):
    """Routing Rule.
    """

    def __init__(self, url_path: str, **kwargs):
        self.call = kwargs.pop('call')
        self.filters = kwargs.pop('filters', ())

        endpoint = kwargs.get('endpoint')
        try:
            _routes.iter_rules(endpoint)
            raise Exception("Endpoint name '{}' already used.".format(endpoint))
        except KeyError:
            super().__init__(url_path, **kwargs)

    def get_rules(self, rules_map):
        return super().get_rules(rules_map)


def get_session_store() -> _FilesystemSessionStore:
    """Get session store.
    """
    return _session_store


def set_request(r: _http.request.Request):
    """Set request for the current thread.
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


def add_rule(pattern: str, name: str = None, call: str = None, args: dict = None, methods=None, filters=None):
    """Add a rule to the router.

    :param methods: str|tuple|list
    """
    if not name and not call:
        raise RuntimeError("Either 'name' or 'call' must be specified.")

    if filters is None:
        filters = []

    if isinstance(filters, str):
        filters = [filters]

    if isinstance(methods, str):
        methods = (methods,)

    if not isinstance(filters, list) and not isinstance(filters, tuple):
        raise TypeError('Filters must be a string, list or tuple. {} given.'.format(repr(filters)))

    if not name:
        name = _util.random_str(32)

    if not call:
        call = name

    if not args:
        args = {}

    args['_name'] = name
    args['_call'] = call

    rule = Rule(
        url_path=pattern,
        endpoint=name,
        call=call,
        defaults=args,
        methods=methods,
        filters=filters
    )

    _routes.add(rule)

    # Bind routes map to corresponding adapter.
    # It is necessary to get ability to build endpoint URLs before dispatch() call.
    tid = _threading.get_id()
    if tid not in _map_adapters:
        _map_adapters[tid] = _routes.bind(server_name())


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


def resolve_ep_callable(ep_name: str) -> callable:
    if '$theme' in ep_name:
        ep_name = ep_name.replace('$theme', _theme.get_current())

    if '@' in ep_name:
        ep_name = ep_name.replace('@', '.ep.')

    return _util.get_callable(ep_name)


def call_ep(ep_name: str, args: dict = None, inp: dict = None):
    """Call a callable.
    """
    if args is not None:
        if '_call' in args:
            args['_call_orig'] = args['_call']
        args['_call'] = ep_name

        if '_name' in args:
            args['_name_orig'] = args['_name']
        args['_name'] = ep_name

        return resolve_ep_callable(ep_name)(args, inp)

    elif inp is not None:
        return resolve_ep_callable(ep_name)(inp)

    else:
        return resolve_ep_callable(ep_name)()


def dispatch(env: dict, start_response: callable):
    """Dispatch a request.
    """
    from pytsite import events
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

    _map_adapters[tid] = _routes.bind_to_environ(env)

    # Remove trailing slash
    path_info = _map_adapters[tid].path_info
    if len(path_info) > 1 and path_info.endswith('/'):
        redirect_url = _re.sub('/$', '', path_info)
        if _map_adapters[tid].query_args:
            redirect_url += '?' + _map_adapters[tid].query_args
        return _http.response.Redirect(redirect_url, 301)(env, start_response)

    # All requests are cached by default
    set_no_cache(False)

    # Detect language from path
    languages = _lang.langs()
    if len(languages) > 1:
        if _re.search('^/[a-z]{2}(/|$)', env['PATH_INFO']):
            # Extract language code as first two-letters of the path
            lang_code = env['PATH_INFO'][1:3]
            try:
                _lang.set_current(lang_code)
                env['PATH_INFO'] = env['PATH_INFO'][3:]
                if not env['PATH_INFO']:
                    env['PATH_INFO'] = '/'
                # If requested language is default, redirect to path without language prefix
                if lang_code == languages[0]:
                    return _http.response.Redirect(env['PATH_INFO'], 301)(env, start_response)
            except _lang.error.LanguageNotSupported:
                # If language is not defined, do nothing. 404 will fired in the code below.
                pass
        else:
            # No language code found in the path. Set first defined language as current.
            _lang.set_current(languages[0])

    # Notify listeners
    events.fire('pytsite.router.pre_dispatch', path_info=env['PATH_INFO'])

    # Loading path alias, if it exists or use current one
    env['PATH_INFO'] = _path_aliases.get(env['PATH_INFO'], env['PATH_INFO'])

    # Replace url adapter with modified environment
    _map_adapters[tid] = _routes.bind_to_environ(env)

    # Creating request context
    set_request(_http.request.Request(env))

    # Shortcuts
    request_input = request().inp
    request_cookies = request().cookies

    # Session setup
    sid = request_cookies.get('PYTSITE_SESSION')
    if sid:
        _sessions[tid] = _session_store.get(sid)
    else:
        _sessions[tid] = _session_store.new()

    # Processing request
    try:
        # Notify listeners
        events.fire('pytsite.router.dispatch')

        # Search for rule
        rule, rule_args = _map_adapters[tid].match(return_rule=True)

        # Processing rule filters
        for flt in rule.filters:
            flt_args = rule_args.copy()
            flt_split = flt.split(':')
            flt_endpoint = flt_split[0]
            if len(flt_split) > 1:
                for flt_arg_str in flt_split[1:]:
                    flt_arg_str_split = flt_arg_str.split('=')
                    if len(flt_arg_str_split) == 2:
                        flt_args[flt_arg_str_split[0]] = flt_arg_str_split[1]

            flt_response = call_ep(flt_endpoint, flt_args, request_input)
            if isinstance(flt_response, _http.response.Redirect):
                return flt_response(env, start_response)

        # Preparing response object
        wsgi_response = _http.response.Response(response='', status=200, content_type='text/html', headers=[])

        # Processing response from handler
        try:
            response_from_callable = call_ep(rule.call, rule_args, request().inp)
        except ImportError as e:
            raise _http.error.NotFound(e)

        if isinstance(response_from_callable, str):
            # Minifying output
            if _reg.get('output.minify'):
                response_from_callable = _util.minify_html(response_from_callable)
            wsgi_response.data = response_from_callable
        elif isinstance(response_from_callable, _http.response.Response):
            wsgi_response = response_from_callable
        else:
            wsgi_response.data = ''

        # Cache control
        if get_no_cache() or request().method != 'GET':
            wsgi_response.headers.set('Cache-Control', 'private, max-age=0, no-cache, no-store')
            wsgi_response.headers.set('Pragma', 'no-cache')
        else:
            wsgi_response.headers.set('Cache-Control', 'public')

        # Store updated session data
        if session().should_save:
            _session_store.save(session())
            wsgi_response.set_cookie('PYTSITE_SESSION', session().sid)

        events.fire('pytsite.router.response', response=wsgi_response)

        return wsgi_response(env, start_response)

    except Exception as e:
        if isinstance(e, _HTTPException):
            # If exception has embedded response in its body
            if isinstance(e.response, _http.response.Response):
                # For non-redirect embedded responses use original status code from exception
                if not isinstance(e.response, _http.response.Redirect):
                    e.response.status_code = e.code

                return e.response(env, start_response)

            code = e.code
            title = _lang.t('pytsite.router@http_error_' + str(e.code))
            _logger.error('HTTP {} {} ({}): {}'.
                          format(e.code, e.name, current_path(resolve_alias=False, strip_lang=False), e.description))
        else:
            code = 500
            title = _lang.t('pytsite.router@error', {'code': '500'})
            _logger.error(e, exc_info=e)

        from pytsite import metatag
        metatag.t_set('title', title)

        args = {
            'title': title,
            'exception': e,
            'traceback': _format_exc()
        }

        events.fire('pytsite.router.exception', args=args)

        # User defined exception handler
        if is_ep_callable('$theme@exception'):
            wsgi_response = call_ep('$theme@exception', args)

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

    if not lang:
        lang = _lang.get_current()
    if lang not in available_langs:
        raise RuntimeError("Language '{}' is not supported.".format(lang))

    r = '/'
    if lang != available_langs[0]:
        r += lang + '/'

    return r


def server_name():
    """Get server's name.
    """
    tid = _threading.get_id()
    if tid in _map_adapters:
        name = _map_adapters[tid].server_name
    else:
        from pytsite import reg
        name = reg.get('server_name', 'localhost')

    return name


def scheme():
    """Get current URL scheme.
    """
    tid = _threading.get_id()

    return _map_adapters[_threading.get_id()].url_scheme if tid in _map_adapters else 'http'


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

    lang = kwargs.get('lang')  # type: str
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
    if not bool(parsed_url[0]) and not strip_lang:
        lang_re = '^/({})/'.format('|'.join(_lang.langs()))
        if not _re.search(lang_re, parsed_url[2]):
            r[2] = str(base_path(lang) + parsed_url[2]).replace('//', '/')

    return _urlparse.urlunparse(r)


def current_path(strip_query=False, resolve_alias=True, strip_lang=True, lang: str = None) -> str:
    """Get current path.
    """
    if not _requests:
        return '/'

    r = _urlparse.urlparse(request().url)
    path = _urlparse.urlunparse(('', '', r[2], r[3], '', ''))
    query = _urlparse.urlunparse(('', '', '', '', r[4], r[5]))

    if resolve_alias:
        for k, v in _path_aliases.items():
            if path == v:
                path = k
                break

    if not strip_lang:
        path = str(base_path(lang) + path).replace('//', '/')

    r = str(path)
    if not strip_query:
        r += str(query)

    return r


def current_url(strip_query: bool = False, resolve_alias: bool = True, lang: str = None, add_query: dict = None,
                add_fragment: str = None) -> str:
    """Get current URL.
    """
    r = scheme() + '://' + server_name() + current_path(strip_query, resolve_alias, False, lang)
    if add_query or add_fragment:
        r = url(r, query=add_query, fragment=add_fragment)

    return r


def ep_path(endpoint: str, route_args: dict = None) -> str:
    """Get path for an endpoint.
    """
    tid = _threading.get_id()
    if tid not in _map_adapters:
        _map_adapters[tid] = _routes.bind(server_name())

    return _map_adapters[tid].build(endpoint, route_args)


def ep_url(ep_name: str, route_args: dict = None, **kwargs) -> str:
    """Get URL for an endpoint.
    """
    return url(ep_path(ep_name, route_args), **kwargs)
