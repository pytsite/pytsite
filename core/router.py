"""Router.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path, makedirs
from traceback import format_exc
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from werkzeug.routing import Map, Rule as _Rule
from werkzeug.exceptions import HTTPException
from werkzeug.contrib.sessions import FilesystemSessionStore
from importlib import import_module
from re import sub
from htmlmin import minify
from .http.request import Request
from .http.response import Response, RedirectResponse
from .http.session import Session
from .http.errors import NotFound
from . import reg, logger

session_storage_path = reg.get('paths.session')
if not path.exists(session_storage_path):
    makedirs(session_storage_path, 0o755, True)

__session_store = FilesystemSessionStore(path=session_storage_path, session_class=Session)

__routes = Map()

__url_adapter = __routes.bind(reg.get('server_name', 'localhost'))

request = None
""":type : pytsite.core.http.request.Request"""

session = None
""":type : pytsite.core.http.session.Session"""


class Rule(_Rule):
    """Routing rule.
    """
    def __init__(self, string: str, **kwargs):
        self.filters = ()
        if 'filters' in kwargs:
            self.filters = kwargs.get('filters', ())
            del kwargs['filters']

        super().__init__(string, **kwargs)


def add_rule(pattern: str, endpoint: str, defaults: dict=None, methods: list=None, redirect_to: str=None,
             filters: tuple=None):
    """Add a rule to the router.
    """

    if filters is None:
        filters = []

    rule = Rule(
        string=pattern,
        endpoint=endpoint,
        defaults=defaults,
        methods=methods,
        redirect_to=redirect_to,
        filters=filters
    )

    __routes.add(rule)


def call_endpoint(name: str, args: dict=None, inp: dict=None):
    endpoint = name.split('.')
    if not len(endpoint):
        raise TypeError("Invalid format of endpoint specification: '{0}'".format(name))

    module_name = '.'.join(endpoint[0:len(endpoint)-1])
    callable_name = endpoint[-1]

    module = import_module(module_name)
    if callable_name not in dir(module):
        logger.error("Callable '{}.{}' is not found.".format(module_name, callable_name))
        raise NotFound()

    callable_obj = getattr(module, callable_name)
    if not hasattr(callable_obj, '__call__'):
        logger.error("'{}.{}' is not callable".format(module_name, callable_name))
        raise NotFound()

    return callable_obj(args, inp)


def dispatch(env: dict, start_response: callable):
    """Dispatch the request.
    """
    from pytsite.core import tpl, metatag, lang, events
    global __url_adapter, __session_store, request, session

    # Replace url adapter with environment-based
    __url_adapter = __routes.bind_to_environ(env)

    request = Request(env)

    # Remove trailing slash
    path_info = __url_adapter.path_info
    if len(path_info) > 1 and path_info.endswith('/'):
        redirect_url = sub(r'/$', '', path_info)
        if __url_adapter.query_args:
            redirect_url += '?' + __url_adapter.query_args
        return RedirectResponse(redirect_url, 301)(env, start_response)

    # Session setup
    sid = request.cookies.get('PYTSITE_SESSION')
    if sid:
        session = __session_store.get(sid)
    else:
        session = __session_store.new()

    try:
        rule, rule_args = __url_adapter.match(return_rule=True)

        events.fire('pytsite.core.router.dispatch')

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

            flt_response = call_endpoint(flt_endpoint, flt_args, request.get_values_dict())
            if isinstance(flt_response, RedirectResponse):
                return flt_response(env, start_response)

        # Processing response from handler
        wsgi_response = Response(response='', status=200, content_type='text/html')
        response_from_callable = call_endpoint(rule.endpoint, rule_args, request.get_values_dict())
        if isinstance(response_from_callable, str):
            if reg.get('output.minify'):
                response_from_callable = minify(response_from_callable, True, True)
            wsgi_response.data = response_from_callable
        elif isinstance(response_from_callable, Response):
            wsgi_response = response_from_callable
        else:
            wsgi_response.data = ''

        # Updating session data
        if session.should_save:
            __session_store.save(session)
            wsgi_response.set_cookie('PYTSITE_SESSION', session.sid)

        return wsgi_response(env, start_response)

    except HTTPException as e:
        metatag.set_tag('title', lang.t('pytsite.core@error', {'code': e.code}))
        wsgi_response = tpl.render('app@exceptions/common', {'exception': e, 'traceback': format_exc()})
        return Response(wsgi_response, e.code, content_type='text/html')(env, start_response)

    except Exception as e:
        metatag.set_tag('title', lang.t('pytsite.core@error', {'code': 500}))
        wsgi_response = tpl.render('app@exceptions/common', {'exception': e, 'traceback': format_exc()})
        logger.error(str(e))
        return Response(wsgi_response, 500, content_type='text/html')(env, start_response)


def base_path(language: str=None)->str:
    """Get base path of application.
    """
    from .lang import get_current_lang, get_languages
    current_lang = get_current_lang()
    available_langs = get_languages()

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
    name = reg.get('console.server_name', 'localhost')
    if __url_adapter:
        name = __url_adapter.server_name

    return name


def scheme():
    r = 'http'
    if __url_adapter:
        r = __url_adapter.url_scheme

    return r


def base_url(language: str=None):
    """Get base URL of application.
    """

    return scheme() + '://' + server_name() + base_path(language)


def url(url: str, lang: str=None, strip_lang=False, query: dict=None) -> str:
    """Generate an URL.
    """

    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
    parsed_url = urlparse(url)
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
        parsed_qs = parse_qs(parsed_url[4])
        parsed_qs.update(query)
        r[4] = urlencode(parsed_qs, doseq=True)

    # Adding language suffix
    if not strip_lang:
        r[2] = str(base_path(lang) + parsed_url[2]).replace('//', '/')

    return urlunparse(r)


def current_url(strip_query_string=False):
    """Get current URL.
    """
    if not request:
        return 'http://' + reg.get('server_name')

    r = request.url
    if strip_query_string:
        r = urlparse(r)
        r = urlunparse((r[0], r[1], r[2], r[3], '', ''))

    return r


def endpoint_url(endpoint: str, args: dict=None)->str:
    """Get URL for endpoint.
    """

    global __url_adapter
    return url(__url_adapter.build(endpoint, args))
