"""Router.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from os import path as _path, makedirs as _makedirs
from traceback import format_exc as _format_exc
from urllib import parse as _urlparse
from werkzeug.routing import Map as _Map, Rule as _Rule
from werkzeug.exceptions import HTTPException as _HTTPException
from werkzeug.contrib.sessions import FilesystemSessionStore as _FilesystemSessionStore
from importlib import import_module as _import_module
from htmlmin import minify as _minify
from . import reg as _reg, logger as _logger, http as _http


session_storage_path = _reg.get('paths.session')
if not _path.exists(session_storage_path):
    _makedirs(session_storage_path, 0o755, True)

__session_store = _FilesystemSessionStore(path=session_storage_path, session_class=_http.session.Session)
__routes = _Map()
__url_adapter = __routes.bind(_reg.get('server_name', 'localhost'))
__path_aliases = {}


request = None
""":type : pytsite.core.http._request.Request"""

session = None
""":type : pytsite.core.http._session.Session"""


class Rule(_Rule):
    """Routing rule.
    """
    def __init__(self, string: str, **kwargs):
        self.filters = ()
        if 'filters' in kwargs:
            self.filters = kwargs.get('filters', ())
            del kwargs['filters']

        super().__init__(string, **kwargs)


def add_rule(pattern: str, endpoint: str, defaults: dict=None, methods: tuple=None, redirect_to: str=None,
             filters=None):
    """Add a rule to the router.
    """
    if filters is None:
        filters = []

    if isinstance(filters, str):
        filters = [filters]

    if not isinstance(filters, list) and not isinstance(filters, tuple):
        raise Exception('Filters must be a string, list or tuple. {} given.'.format(repr(filters)))

    rule = Rule(
        string=pattern,
        endpoint=endpoint,
        defaults=defaults,
        methods=methods,
        redirect_to=redirect_to,
        filters=filters
    )

    __routes.add(rule)


def add_path_alias(alias: str, target: str):
    __path_aliases[alias] = target


def call_endpoint(name: str, args: dict=None, inp: dict=None):
    """Call an endpoint.
    """
    endpoint = name.split('.')
    if not len(endpoint):
        raise TypeError("Invalid format of endpoint specification: '{0}'".format(name))

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
    from pytsite.core import tpl, metatag, events, lang
    global __url_adapter, request, session

    if _path.exists(_reg.get('paths.maintenance.lock')):
        wsgi_response = _http.response.Response(response='We are in maintenance mode now. Please try again later.',
                                                status=503, content_type='text/html')
        return wsgi_response(env, start_response)

    # Detect language from path
    languages = lang.get_langs()
    if len(languages) > 1:
        if _re.match(r'/[a-z]{2}(/|$)', env['PATH_INFO']):
            lang_code = env['PATH_INFO'][1:3]
            lang.set_current_lang(lang_code)
            env['PATH_INFO'] = env['PATH_INFO'][4:]
            if lang_code == languages[0]:
                return _http.response.RedirectResponse(env['PATH_INFO'], 301)(env, start_response)
        else:
            lang.set_current_lang(languages[0])

    # Notify listeners
    events.fire('pytsite.core.router.pre_dispatch', path_info=env['PATH_INFO'])

    # Loading path alias
    env['PATH_INFO'] = __path_aliases.get(env['PATH_INFO'], env['PATH_INFO'])

    # Replace url adapter with environment-based
    __url_adapter = __routes.bind_to_environ(env)

    # Creating request
    request = _http.request.Request(env)

    # Remove trailing slash
    path_info = __url_adapter.path_info
    if len(path_info) > 1 and path_info.endswith('/'):
        redirect_url = _re.sub(r'/$', '', path_info)
        if __url_adapter.query_args:
            redirect_url += '?' + __url_adapter.query_args
        return _http.response.RedirectResponse(redirect_url, 301)(env, start_response)

    # Session setup
    sid = request.cookies.get('PYTSITE_SESSION')
    if sid:
        session = __session_store.get(sid)
    else:
        session = __session_store.new()

    try:
        rule, rule_args = __url_adapter.match(return_rule=True)

        # Notify listeners
        events.fire('router.dispatch')

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

            flt_response = call_endpoint(flt_endpoint, flt_args, request.values_dict)
            if isinstance(flt_response, _http.response.RedirectResponse):
                return flt_response(env, start_response)

        # Processing response from handler
        wsgi_response = _http.response.Response(response='', status=200, content_type='text/html')
        response_from_callable = call_endpoint(rule.endpoint, rule_args, request.values_dict)
        if isinstance(response_from_callable, str):
            if _reg.get('output.minify'):
                response_from_callable = _minify(response_from_callable, True, True)
            wsgi_response.data = response_from_callable
        elif isinstance(response_from_callable, _http.response.Response):
            wsgi_response = response_from_callable
        else:
            wsgi_response.data = ''

        # Updating session data
        if session.should_save:
            __session_store.save(session)
            wsgi_response.set_cookie('PYTSITE_SESSION', session.sid)

        return wsgi_response(env, start_response)

    except _HTTPException as e:
        metatag.t_set('title', lang.t('core@error', {'code': e.code}))
        wsgi_response = tpl.render('app@exceptions/common', {'exception': e, 'traceback': _format_exc()})
        return _http.response.Response(wsgi_response, e.code, content_type='text/html')(env, start_response)

    except Exception as e:
        metatag.t_set('title', lang.t('core@error', {'code': 500}))
        wsgi_response = tpl.render('app@exceptions/common', {'exception': e, 'traceback': _format_exc()})
        _logger.error(str(e))
        return _http.response.Response(wsgi_response, 500, content_type='text/html')(env, start_response)


def base_path(language: str=None) -> str:
    """Get base path of application.
    """
    from .lang import get_current_lang, get_langs
    current_lang = get_current_lang()
    available_langs = get_langs()

    if not language:
        language = get_current_lang()

    if language not in available_langs:
        raise Exception("Language '{0}' is not supported.".format(language))

    r = '/'
    if len(available_langs) > 1 and language != current_lang:
        r += language + '/'

    return r


def server_name():
    from . import reg
    name = reg.get('server_name', 'localhost')
    if __url_adapter:
        name = __url_adapter.server_name

    return name


def scheme():
    r = 'http'
    if __url_adapter:
        r = __url_adapter.url_scheme

    return r


def base_url(language: str=None, query: dict=None):
    """Get base URL of application.
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
    if not strip_lang:
        r[2] = str(base_path(lang) + parsed_url[2]).replace('//', '/')

    r = _urlparse.urlunparse(r)

    if relative:
        r = _re.sub(r'^https?://[\w\.\-]+/', '/', r)

    if strip_query:
        r = _re.sub(r'\?.+', '', r)

    return r


def current_path(strip_query: bool=False, resolve_alias: bool=True) -> str:
    """Get current path.
    """
    if not request:
        return '/'

    r = _urlparse.urlparse(request.url)
    path = _urlparse.urlunparse(('', '', r[2], r[3], '', ''))
    query = _urlparse.urlunparse(('', '', '', '', r[4], r[5]))

    if resolve_alias:
        for k, v in __path_aliases.items():
            if path == v:
                path = k
                break

    r = str(path)
    if not strip_query:
        r += str(query)

    return r


def current_url(strip_query: bool=False, resolve_alias: bool=True) -> str:
    """Get current URL.
    """
    return scheme() + '://' + server_name() + current_path(strip_query, resolve_alias)


def endpoint_url(endpoint: str, args: dict=None, relative: bool=False) -> str:
    """Get URL for endpoint.
    """
    return url(__url_adapter.build(endpoint, args), relative=relative)
