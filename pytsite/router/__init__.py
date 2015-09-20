"""PytSite Router.
"""
import re as _re
from os import path as _path, makedirs as _makedirs
from traceback import format_exc as _format_exc
from urllib import parse as _urlparse
from importlib import import_module as _import_module
from werkzeug.routing import Map as _Map, Rule as _Rule
from werkzeug.exceptions import HTTPException as _HTTPException
from werkzeug.contrib.sessions import FilesystemSessionStore as _FilesystemSessionStore
from htmlmin import minify as _minify
from pytsite import reg as _reg, logger as _logger, http as _http, util as _util, lang as _lang, events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_routes = _Map()
_url_adapter = _routes.bind(_reg.get('server.name', 'localhost'))
_path_aliases = {}

# Registering module's language package
_lang.register_package(__name__)

# Create directory to store session data
session_storage_path = _reg.get('paths.session')
if not _path.exists(session_storage_path):
    _makedirs(session_storage_path, 0o755, True)

# Initializing session store
_session_store = _FilesystemSessionStore(path=session_storage_path, session_class=_http.session.Session)

# Enable or disable cache
no_cache = False

# Request object
request = None
""":type : pytsite.http._request.Request"""

# Session object
session = None
""":type : pytsite.http._session.Session"""


class Rule(_Rule):
    """Routing Rule.
    """
    def __init__(self, url_path: str, **kwargs):
        self.call = kwargs.get('call')
        self.filters = kwargs.get('filters', ())

        endpoint = kwargs.get('endpoint')
        try:
            _routes.iter_rules(endpoint)
            raise Exception("Endpoint name '{}' already used.".format(endpoint))
        except KeyError:
            del kwargs['call']
            del kwargs['filters']
            super().__init__(url_path, **kwargs)

    def get_rules(self, rules_map):
        return super().get_rules(rules_map)


def add_rule(pattern: str, name: str=None, call: str=None, args: dict=None, methods=None, filters=None):
    """Add a rule to the router.
    :param methods: str|tuple|list
    """
    if not name and not call:
        raise Exception("Either 'name' or 'call' must be specified.")

    if filters is None:
        filters = []

    if isinstance(filters, str):
        filters = [filters]

    if isinstance(methods, str):
        methods = (methods, )

    if not isinstance(filters, list) and not isinstance(filters, tuple):
        raise Exception('Filters must be a string, list or tuple. {} given.'.format(repr(filters)))

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


def add_path_alias(alias: str, target: str):
    _path_aliases[alias] = target


def call_ep(name: str, args: dict=None, inp: dict=None):
    """Call an endpoint.
    """
    endpoint = name.split('.')
    if not len(endpoint):
        raise TypeError("Invalid format of endpoint specification: '{}'".format(name))

    module_name = '.'.join(endpoint[0:len(endpoint)-1])
    callable_name = endpoint[-1]

    module = _import_module(module_name)
    if callable_name not in dir(module):
        raise Exception("'{}.{}' is not callable".format(module_name, callable_name))

    callable_obj = getattr(module, callable_name)
    if not hasattr(callable_obj, '__call__'):
        raise Exception("'{}.{}' is not callable".format(module_name, callable_name))

    return callable_obj(args, inp)


def dispatch(env: dict, start_response: callable):
    """Dispatch the request.
    """
    from pytsite import tpl, metatag, events
    global _url_adapter, request, session, no_cache

    if _path.exists(_reg.get('paths.maintenance.lock')):
        wsgi_response = _http.response.Response(response='We are in maintenance mode now. Please try again later.',
                                                status=503, content_type='text/html')
        return wsgi_response(env, start_response)

    # Remove trailing slash
    _url_adapter = _routes.bind_to_environ(env)
    path_info = _url_adapter.path_info
    if len(path_info) > 1 and path_info.endswith('/'):
        redirect_url = _re.sub('/$', '', path_info)
        if _url_adapter.query_args:
            redirect_url += '?' + _url_adapter.query_args
        return _http.response.Redirect(redirect_url, 301)(env, start_response)

    # All requests are cached by default
    no_cache = False

    # Detect language from path
    languages = _lang.get_langs()
    if len(languages) > 1:
        if _re.search('^/[a-z]{2}(/|$)', env['PATH_INFO']):
            lang_code = env['PATH_INFO'][1:3]
            _lang.set_current_lang(lang_code)
            env['PATH_INFO'] = env['PATH_INFO'][3:]
            if not env['PATH_INFO']:
                env['PATH_INFO'] = '/'
            if lang_code == languages[0]:
                return _http.response.Redirect(env['PATH_INFO'], 301)(env, start_response)
        else:
            # Set first defined language as default
            _lang.set_current_lang(languages[0])

    # Notify listeners
    events.fire('pytsite.router.pre_dispatch', path_info=env['PATH_INFO'])

    # Loading path alias
    env['PATH_INFO'] = _path_aliases.get(env['PATH_INFO'], env['PATH_INFO'])

    # Replace url adapter with modified environment
    _url_adapter = _routes.bind_to_environ(env)

    # Creating request
    request = _http.request.Request(env)

    # Session setup
    sid = request.cookies.get('PYTSITE_SESSION')
    if sid:
        session = _session_store.get(sid)
    else:
        session = _session_store.new()

    try:
        rule, rule_args = _url_adapter.match(return_rule=True)

        # Notify listeners
        events.fire('pytsite.router.dispatch')

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

            flt_response = call_ep(flt_endpoint, flt_args, request.values_dict)
            if isinstance(flt_response, _http.response.Redirect):
                return flt_response(env, start_response)

        wsgi_response = _http.response.Response(response='', status=200, content_type='text/html', headers=[])

        # Processing response from handler
        response_from_callable = call_ep(rule.call, rule_args, request.values_dict)
        if isinstance(response_from_callable, str):
            if _reg.get('output.minify'):
                response_from_callable = _minify(response_from_callable, True, True)
            wsgi_response.data = response_from_callable
        elif isinstance(response_from_callable, _http.response.Response):
            wsgi_response = response_from_callable
        else:
            wsgi_response.data = ''

        # Cache control
        if no_cache or request.method != 'GET':
            wsgi_response.headers.set('Cache-Control', 'private, max-age=0, no-cache, no-store')
            wsgi_response.headers.set('Pragma', 'no-cache')
        else:
            wsgi_response.headers.set('Cache-Control', 'public')

        # Updating session data
        if session.should_save:
            _session_store.save(session)
            wsgi_response.set_cookie('PYTSITE_SESSION', session.sid)

        return wsgi_response(env, start_response)

    except _HTTPException as e:
        try:
            title = _lang.t('http_error_' + str(e.code))
        except _lang.error.TranslationError:
            title = _lang.t('pytsite.router@error', {'code': str(e.code)})

        metatag.t_set('title', title)

        wsgi_response = tpl.render('exceptions/common', {
            'title': title,
            'exception': e,
            'traceback': _format_exc()
        })

        return _http.response.Response(wsgi_response, e.code, content_type='text/html')(env, start_response)

    except Exception as e:
        _logger.error(str(e), __name__)

        title = _lang.t('pytsite.router@error', {'code': '500'})
        metatag.t_set('title', title)

        wsgi_response = tpl.render('exceptions/common', {
            'title': title,
            'exception': e,
            'traceback': _format_exc()
        })

        return _http.response.Response(wsgi_response, 500, content_type='text/html')(env, start_response)


def base_path(language: str=None) -> str:
    """Get base path of application.
    """
    from pytsite import lang
    available_langs = lang.get_langs()

    if len(available_langs) == 1:
        return '/'

    if not language:
        language = lang.get_current_lang()
    if language not in available_langs:
        raise Exception("Language '{}' is not supported.".format(language))

    r = '/'
    if language != available_langs[0]:
        r += language + '/'

    return r


def server_name():
    """Get server's name.
    """
    from pytsite import reg
    name = reg.get('server.name', 'localhost')
    if _url_adapter:
        name = _url_adapter.server_name

    return name


def scheme():
    """Get current URL scheme.
    """
    r = 'http'
    if _url_adapter:
        r = _url_adapter.url_scheme

    return r


def base_url(language: str=None, query: dict=None):
    """Get base URL of the application.
    """
    r = scheme() + '://' + server_name() + base_path(language)
    if query:
        r = url(r, query=query)

    return r


def is_base_url(compare: str=None) -> bool:
    """Check if the given URL is base.
    """
    if not compare:
        compare = current_url(True)

    return base_url() == compare


def url(url_str: str, lang: str=None, strip_lang=False, query: dict=None, relative: bool=False,
        strip_query=False) -> str:
    """Generate an URL.
    """
    if not url_str:
        raise ValueError('url_str cannot be empty.')

    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
    parsed_url = _urlparse.urlparse(url_str)
    r = [
        parsed_url[0] if parsed_url[0] else scheme(),  # 0, Scheme
        parsed_url[1] if parsed_url[1] else server_name(),  # 1, Netloc
        parsed_url[2] if parsed_url[2] else '',  # 2, Path
        parsed_url[3] if parsed_url[3] else '',  # 3, Params
        parsed_url[4] if parsed_url[4] else '',  # 4, Query
        parsed_url[5] if parsed_url[5] else '',  # 5, Fragment
    ]

    # Attaching additional query arguments
    if query:
        parsed_qs = _urlparse.parse_qs(parsed_url[4])
        parsed_qs.update(query)
        r[4] = _urlparse.urlencode(parsed_qs, doseq=True)

    # Adding language suffix
    if not strip_lang and not _re.search('^/[a-z]{2}/', parsed_url[2]):
        r[2] = str(base_path(lang) + parsed_url[2]).replace('//', '/')

    r = _urlparse.urlunparse(r)

    if relative:
        r = _re.sub(r'^https?://[\w\.\-]+/', '/', r)

    if strip_query:
        r = _re.sub('\?.+', '', r)

    return r


def current_path(strip_query=False, resolve_alias=True, strip_lang=True) -> str:
    """Get current path.
    """
    if not request:
        return '/'

    r = _urlparse.urlparse(request.url)
    path = _urlparse.urlunparse(('', '', r[2], r[3], '', ''))
    query = _urlparse.urlunparse(('', '', '', '', r[4], r[5]))

    if resolve_alias:
        for k, v in _path_aliases.items():
            if path == v:
                path = k
                break

    if not strip_lang:
        path = str(base_path() + path).replace('//', '/')

    r = str(path)
    if not strip_query:
        r += str(query)

    return r


def current_url(strip_query: bool=False, resolve_alias: bool=True) -> str:
    """Get current URL.
    """
    return scheme() + '://' + server_name() + current_path(strip_query, resolve_alias, False)


def en_path(endpoint: str, args: dict=None) -> str:
    return url(_url_adapter.build(endpoint, args), relative=True)


def ep_url(ep_name: str, args: dict=None, strip_lang=False) -> str:
    """Get URL for endpoint.
    """
    r = _url_adapter.build(ep_name, args)
    return url(r, strip_lang=strip_lang, relative=False)
