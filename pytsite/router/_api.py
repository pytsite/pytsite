"""PytSite Router API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from typing import Dict, Union, List, Mapping, Optional, Type, Tuple
from traceback import format_exc
from urllib import parse as urlparse
from werkzeug.contrib.sessions import FilesystemSessionStore
from pytsite import reg, logger, http, util, lang as lang_api, tpl, threading, events, routing, maintenance, errors

_LANG_CODE_RE = _re.compile('^/[a-z]{2}(/|$)')

# Rules map
_rules = routing.RulesMap()

# Path aliases
_path_aliases = {}

# Session store
_session_store = FilesystemSessionStore(path=reg.get('paths.session'), session_class=http.Session)

# Thread safe requests collection
_requests = {}  # type: Dict[int, http.Request]

# Thread safe sessions collection
_sessions = {}  # type: Dict[int, http.Session]

# Thread safe 'no-cache' statues collection
_no_cache = {}  # type: Dict[int, bool]


def get_session_store() -> FilesystemSessionStore:
    """Get session store
    """
    return _session_store


def set_request(r: http.Request):
    """Set request for current thread
    """
    _requests[threading.get_id()] = r

    return r


def request() -> Optional[http.Request]:
    """Get request of current thread
    """
    return _requests.get(threading.get_id())


def session() -> http.Session:
    """Get session object
    """
    return _sessions.get(threading.get_id())


def delete_session():
    """Delete session data from storage
    """
    _session_store.delete(session())


def no_cache(state: bool = None) -> Optional[bool]:
    """Get/set 'no-cache' status belonged to the current thread
    """
    if state is None:
        return _no_cache.get(threading.get_id())
    else:
        _no_cache[threading.get_id()] = state


def handle(controller: Union[str, Type[routing.Controller]], path: str = None, name: str = None,
           defaults: dict = None, methods: Union[str, Tuple[str, ...]] = 'GET',
           filters: Union[Type[routing.Filter], Tuple[Type[routing.Filter]]] = None):
    """Add a rule to the router
    """
    if isinstance(controller, str):
        controller = _rules.get(controller).controller_class

    if filters is not None and issubclass(filters, routing.Filter):
        filters = (filters,)

    _rules.add(routing.Rule(controller, path, name, defaults, methods, filters))


def add_path_alias(alias: str, target: str):
    """Add an alias for a path
    """
    _path_aliases[alias] = target


def remove_path_alias(alias: str):
    """Remove an alias for a path
    """
    if alias in _path_aliases:
        del _path_aliases[alias]


def has_rule(rule_name: str) -> bool:
    """Check if the rule is registered
    """
    return _rules.has(rule_name)


def call(rule_name: str, args: Mapping, http_request: http.Request = None):
    """Call a controller
    """
    c = _rules.get(rule_name).controller_class()  # type: routing.Controller
    c.request = http_request or request()
    c.args.update(args)
    c.args.validate()

    return c.exec()


def dispatch(env: dict, start_response: callable):
    """Dispatch a request
    """
    tid = threading.get_id()

    # Check maintenance mode status
    if maintenance.is_enabled():
        wsgi_response = http.Response(response=lang_api.t('pytsite.router@we_are_in_maintenance'), status=503,
                                      content_type='text/html')
        return wsgi_response(env, start_response)

    # Remove trailing slash
    if env['PATH_INFO'] != '/' and env['PATH_INFO'].endswith('/'):
        redirect_url = _re.sub('/$', '', env['PATH_INFO'])
        redirect_url += '?' + env['QUERY_STRING'] if env['QUERY_STRING'] else ''
        return http.RedirectResponse(redirect_url, 301)(env, start_response)

    # All requests are cached by default
    no_cache(False)

    # Detect language from path
    languages = lang_api.langs()
    if len(languages) > 1:
        if _LANG_CODE_RE.search(env['PATH_INFO']):
            # Extract language code as first two-letters of the path
            lang_code = env['PATH_INFO'][1:3]
            try:
                lang_api.set_current(lang_code)
                env['PATH_INFO'] = env['PATH_INFO'][3:]
                if not env['PATH_INFO']:
                    env['PATH_INFO'] = '/'
                # If requested language is default, redirect to path without language prefix
                if lang_code == languages[0]:
                    return http.RedirectResponse(env['PATH_INFO'], 301)(env, start_response)
            except lang_api.error.LanguageNotSupported:
                # If language is not defined, do nothing. 404 will be fired in the code below.
                pass
        else:
            # No language code found in the path. Set first defined language as current.
            lang_api.set_current(languages[0])

    # Create request context
    req = set_request(http.Request(env))

    # Notify listeners about incoming request
    if req.is_xhr:
        events.fire('pytsite.router@xhr_pre_dispatch.{}'.format(req.method.lower()))
    else:
        events.fire('pytsite.router@pre_dispatch.{}'.format(req.method.lower()))

    # Get path alias, if it exists, then re-create request context
    if env['PATH_INFO'] in _path_aliases:
        env['PATH_INFO'] = _path_aliases[env['PATH_INFO']]
        req = set_request(http.Request(env))

    # Session setup
    sid = req.cookies.get('PYTSITE_SESSION')
    if sid:
        _sessions[tid] = _session_store.get(sid)
    else:
        _sessions[tid] = _session_store.new()

    # Processing request
    try:
        # Notify listeners about incoming request
        if req.is_xhr:
            events.fire('pytsite.router@xhr_dispatch.{}'.format(req.method.lower()))
        else:
            events.fire('pytsite.router@dispatch.{}'.format(req.method.lower()))

        # Search for the rule
        try:
            rule = _rules.match(req.path, req.method)[0]
        except routing.error.RuleNotFound as e:
            raise http.error.NotFound(e)

        # Instantiate filters
        filters = []  # type: List[routing.Filter]
        for flt_controller_class in rule.filters:  # type: Type[routing.Filter]
            flt = flt_controller_class()  # type: routing.Filter
            flt.request = req
            flt.args.update(req.inp)  # It's important not to overwrite rule's args with input
            flt.args.update(rule.args)  # It's important not to overwrite rule's args with input
            flt.args.validate()
            filters.append(flt)

        # Processing filters before() hook
        for flt in filters:
            flt_response = flt.before()
            if isinstance(flt_response, http.Response):
                return flt_response(env, start_response)

        # Prepare response object
        wsgi_response = http.Response(response='', status=200, content_type='text/html', headers=[])

        # Instantiate controller and fill its arguments
        controller = rule.controller_class()  # type: routing.Controller
        controller.request = req
        controller.args.update(req.inp)  # It's important not to overwrite rule's args with input
        controller.args.update(rule.args)  # It's important not to overwrite rule's args with input
        controller.args['_pytsite_router_rule_name'] = rule.name
        controller.args.validate()

        # Call controller
        try:
            controller_resp = controller.exec()

        # Controllers may call other controllers, and they can generate exceptions
        except routing.error.RuleNotFound as e:
            raise http.error.NotFound(e)

        # Check response from the handler
        if isinstance(controller_resp, str):
            # Minify output
            if reg.get('output.minify'):
                controller_resp = util.minify_html(controller_resp)
            wsgi_response.data = controller_resp
        elif isinstance(controller_resp, http.Response):
            wsgi_response = controller_resp
        else:
            wsgi_response.data = ''

        # Cache control
        if no_cache() or req.method != 'GET':
            wsgi_response.headers.set('Cache-Control', 'private, max-age=0, no-cache, no-store')
            wsgi_response.headers.set('Pragma', 'no-cache')
        else:
            wsgi_response.headers.set('Cache-Control', 'public')

        # Processing filters after() hook
        for flt in filters:
            flt.response = wsgi_response
            flt.after()

        if session().should_save:
            # Store updated session data
            _session_store.save(session())
            wsgi_response.set_cookie('PYTSITE_SESSION', session().sid)
        elif not session() and 'PYTSITE_SESSION' in request().cookies:
            # Delete session cookie in case of empty session
            wsgi_response.delete_cookie('PYTSITE_SESSION')
            _session_store.delete(session())

        if req.is_xhr:
            events.fire('pytsite.router@xhr_response.{}'.format(req.method.lower()), response=wsgi_response)
        else:
            events.fire('pytsite.router@response.{}'.format(req.method.lower()), response=wsgi_response)

        return wsgi_response(env, start_response)

    except Exception as e:
        if isinstance(e, errors.ForbidOperation):
            e = http.error.Forbidden()

        if isinstance(e, http.error.E4xx):
            code = e.code
            title = lang_api.t('pytsite.router@http_error_' + str(e.code))

            logger.error('HTTP {} {} ({}): {}'.format(
                e.code, e.name, current_path(False), e.description))
        else:
            code = e.code if isinstance(e, http.error.E5xx) else 500
            title = lang_api.t('pytsite.router@error', {'code': code})
            logger.error(e)

        args = {
            'title': title,
            'exception': e,
            'traceback': format_exc()
        }

        # Notify listeners
        events.fire('pytsite.router@exception', args=args)

        # User defined exception handler
        if has_rule('pytsite_router_exception'):
            wsgi_response = call('pytsite_router_exception', args)

        # Builtin exception handler
        else:
            try:
                # Try to render user defined template
                wsgi_response = tpl.render('exception', args)
            except tpl.error.TemplateNotFound:
                try:
                    # Default template
                    wsgi_response = tpl.render('pytsite.router@exception', args)
                except tpl.error.TemplateNotFound:
                    # Default simple template
                    wsgi_response = tpl.render('pytsite.router@exception-simple', args)

        return http.Response(wsgi_response, code, content_type='text/html')(env, start_response)


def scheme():
    """Get HTTP scheme
    """
    r = request()

    return r.scheme if (r and r.scheme) else ('https' if reg.get('router.https') else 'http')


def server_name(use_main: bool = False):
    """Get server's name
    """
    r = request()

    return r.host if r and not use_main else reg.get('server_name', 'localhost')


def is_main_host(host_str: str = None) -> bool:
    """Check if the current request's host is the same as defined in app's configuration
    """
    return server_name(True) == (host_str or request().host)


def base_path(lang: str = None) -> str:
    """Get base path of application.
    """
    langs = lang_api.langs()
    if len(langs) == 1:
        return '/'

    lang = lang or lang_api.get_current()

    if lang not in langs:
        raise RuntimeError("Language '{}' is not supported".format(lang))

    return '/' if lang == lang_api.get_primary() else '/' + lang


def url(s: str = '', **kwargs) -> Union[str, list]:
    """Generate an URL
    """
    lang_re = _re.compile('^/({})/'.format('|'.join(lang_api.langs())))

    sch = kwargs.get('scheme', scheme())  # type: str
    use_main_host = kwargs.get('use_main_host', False)
    host = kwargs.get('host', server_name(use_main_host))
    lang = kwargs.get('lang', lang_api.get_current())  # type: str
    add_lang_prefix = kwargs.get('add_lang_prefix', True)  # type: bool
    strip_query = kwargs.get('strip_query', False)  # type: bool
    query = kwargs.get('query')  # type: dict
    relative = kwargs.get('relative', False)  # type: bool
    strip_fragment = kwargs.get('strip_fragment', False)  # type: bool
    fragment = kwargs.get('fragment', '')  # type: str
    as_list = kwargs.get('as_list', False)

    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
    parsed_url = urlparse.urlparse(s)
    r = [
        parsed_url[0] or sch,  # 0, Scheme
        parsed_url[1] or host,  # 1, Netloc
        parsed_url[2] or '',  # 2, Path
        parsed_url[3] or '',  # 3, Params
        parsed_url[4] or '',  # 4, Query
        parsed_url[5] or '',  # 5, Fragment
    ]

    if relative:
        r[0] = ''
        r[1] = ''

    if strip_query:
        # Stripping query
        r[4] = ''
    elif query:
        # Attaching additional query arguments
        parsed_qs = urlparse.parse_qs(parsed_url[4])
        parsed_qs.update(query)
        r[4] = urlparse.urlencode(parsed_qs, doseq=True)

    # Fragment
    r[5] = '' if strip_fragment else urlparse.quote_plus(r[5] + fragment)

    # Add language prefix to the path
    if add_lang_prefix:
        # If language is not already in URL and if language is not a primary one
        if not lang_re.search(parsed_url[2]) and lang != lang_api.get_primary():
            b_path = base_path(lang)
            if not b_path.endswith('/') and not parsed_url[2].startswith('/'):
                b_path += '/'
            r[2] = str(b_path + parsed_url[2]).replace('//', '/')

    # Strip language prefix from the path
    elif lang_re.search(parsed_url[2]):
        r[2] = lang_re.sub('/', parsed_url[2])

    # Remove unwanted slashes from the end of the path
    r[2] = r[2].rstrip('/')

    return urlparse.urlunparse(r) if not as_list else r


def base_url(lang: str = None, query: dict = None, fragment: str = '', use_main_host: bool = False):
    """Get base URL
    """
    return url(lang=lang, query=query, fragment=fragment, use_main_host=use_main_host)


def is_base_url(s: str = None) -> bool:
    """Check if the given URL is the base one
    """
    return base_url() == (s or current_url(True))


def current_path(resolve_alias: bool = True, add_lang_prefix: bool = True, lang: str = None) -> str:
    """Get current path.
    """
    lang = lang or lang_api.get_current()
    req = request()

    r = req.path if req else '/'

    if resolve_alias:
        for alias, target in _path_aliases.items():
            if r == target:
                r = alias
                break

    if add_lang_prefix and lang != lang_api.get_primary():
        r = '/' + lang + (r if r != '/' else '')

    return r


def current_url(strip_query: bool = False, resolve_alias: bool = True, add_lang_prefix: bool = True, lang: str = None,
                query: dict = None, fragment: str = '', use_main_host: bool = False) -> str:
    """Get current URL
    """
    # Update query with request's query
    if not strip_query and request():
        query = query or {}
        query.update(urlparse.parse_qs(request().query_string.decode('utf-8')))

    return url(current_path(resolve_alias, False), strip_query=strip_query, add_lang_prefix=add_lang_prefix, lang=lang,
               query=query, fragment=fragment, use_main_host=use_main_host)


def rule_path(rule_name: str, args: dict = None) -> str:
    """Get path of a rule
    """
    return _rules.path(rule_name, args)


def rule_url(rule_name: str, rule_args: dict = None, **kwargs) -> str:
    """Get URL of a rule
    """
    return url(rule_path(rule_name, rule_args), **kwargs)


def on_pre_dispatch(handler, priority: int = 0, method: str = 'get'):
    """Shortcut
    """
    events.listen('pytsite.router@pre_dispatch.{}'.format(method.lower()), handler, priority)


def on_xhr_pre_dispatch(handler, priority: int = 0, method: str = 'get'):
    """Shortcut
    """
    events.listen('pytsite.router@xhr_pre_dispatch.{}'.format(method.lower()), handler, priority)


def on_dispatch(handler, priority: int = 0, method: str = 'get'):
    """Shortcut
    """
    events.listen('pytsite.router@dispatch.{}'.format(method.lower()), handler, priority)


def on_xhr_dispatch(handler, priority: int = 0, method: str = 'get'):
    """Shortcut
    """
    events.listen('pytsite.router@xhr_dispatch.{}'.format(method.lower()), handler, priority)


def on_response(handler, priority: int = 0, method: str = 'get'):
    """Shortcut
    """
    events.listen('pytsite.router@response.{}'.format(method.lower()), handler, priority)


def on_xhr_response(handler, priority: int = 0, method: str = 'get'):
    """Shortcut
    """
    events.listen('pytsite.router@xhr_response.{}'.format(method.lower()), handler, priority)


def on_exception(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.router@exception', handler, priority)
