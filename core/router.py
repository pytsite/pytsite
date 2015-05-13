__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from traceback import format_exc
from urllib.parse import urlparse, urlunparse
from werkzeug.routing import Map, MapAdapter, Rule as _Rule, BuildError
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Request as _Request, Response as _Response
from werkzeug.contrib.sessions import FilesystemSessionStore, Session
from importlib import import_module
from re import sub
from . import reg

__session_store = FilesystemSessionStore(path=reg.get_val('paths.tmp'))

__routes = Map()

__url_adapter = None
""":type : MapAdapter"""

request = None
""":type : Request"""

session = __session_store.new()
""":type : Session"""


class Rule(_Rule):
    def __init__(self, string: str, **kwargs):
        self.filters = ()
        if 'filters' in kwargs:
            self.filters = kwargs.get('filters', ())
            del kwargs['filters']

        super().__init__(string, **kwargs)


class Request(_Request):
    """HTTP request.
    """
    def get_values(self)->dict:
        """Get all values of the request.
        """
        return self.values.to_dict()

    def get_value(self, key: str, default=None):
        """Get single value of the request.
        """
        return self.values.get(key, default)


class Response(_Response):
    """HTTP response.
    """
    pass


class RedirectResponse(Response):
    """Redirect HTTP response.
    """
    def __init__(self, location: str, status: int=302):
        """Init.
        """
        headers = {'Location': location}
        super().__init__('Redirecting to {0}'.format(location), status=status, headers=headers)


def add_rule(pattern: str, endpoint: str, defaults: dict=None, methods: list=None, redirect_to: str=None,
             filters: list=None):
    """Add a rule to the router.
    """
    rule = Rule(
        string=pattern,
        endpoint=endpoint,
        defaults=defaults,
        methods=methods,
        redirect_to=redirect_to,
        filters=filters
    )

    __routes.add(rule)


def __call_endpoint(name: str, args: dict=None):
    endpoint = name.split('.')
    if not len(endpoint):
        raise TypeError("Invalid format of endpoint specification: '{0}'".format(name))

    module_name = '.'.join(endpoint[0:len(endpoint)-1])
    callable_name = endpoint[-1]

    try:
        module = import_module(module_name)
        if callable_name not in dir(module):
            raise Exception("Callable {0} doesn't exists in module {1}.".format(callable_name, module_name))

        callable_obj = getattr(module, callable_name)
        if not hasattr(callable_obj, '__call__'):
            raise Exception("'{0}' is not callable".format(callable_name))

        return callable_obj(args, request.get_values())

    except ImportError as e:
        e.msg = "Cannot load module '{0}' specified in endpoint '{1}': {2}.".format(module_name, endpoint, e.msg)
        raise e


def dispatch(env: dict, start_response: callable):
    """Dispatch the request.
    """
    from pytsite.core import tpl, metatag, lang
    global __url_adapter, __session_store, request, session

    __url_adapter = __routes.bind_to_environ(env)
    request = Request(env)

    # Remove trailing slash
    path_info = __url_adapter.path_info
    if len(path_info) > 1 and path_info.endswith('/'):
        redirect_url = sub(r'/$', '', path_info)
        if __url_adapter.query_args:
            redirect_url += '?' + __url_adapter.query_args
        return RedirectResponse(redirect_url, 301)(env, start_response)

    # Creating new or restoring existing session
    sid = request.cookies.get('PYTSITE_SESSION')
    if sid:
        session = __session_store.get(sid)

    try:
        rule, args = __url_adapter.match(return_rule=True)

        # Processing rule filters
        if isinstance(rule.filters, list):
            for flt in rule.filters:
                flt_response = __call_endpoint(flt, args)
                if isinstance(flt_response, RedirectResponse):
                    return flt_response(env, start_response)

        # Call endpoint
        response_from_callable = __call_endpoint(rule.endpoint, args)

        response = Response(response='', status=200, content_type='text/html')
        if isinstance(response_from_callable, str):
            response.data = response_from_callable
        elif isinstance(response_from_callable, Response):
            response = response_from_callable
        else:
            response.data = ''

        if session.should_save:
            __session_store.save(session)
            response.set_cookie('PYTSITE_SESSION', session.sid)

        return response(env, start_response)

    except HTTPException as e:
        response = tpl.render('app@exceptions/common', {'exception': e})
        metatag.set_tag('title', lang.t('pytsite.core@error', {'code': e.code}))
        return Response(response, e.code, content_type='text/html')(env, start_response)

    except Exception as e:
        response = tpl.render('app@exceptions/common', {'exception': e, 'traceback': format_exc()})
        metatag.set_tag('title', lang.t('pytsite.core@error', {'code': 500}))
        return Response(response, 500, content_type='text/html')(env, start_response)


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
    name = reg.get_val('console.server_name', 'localhost')
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


def url(url_str: str, language: str=None, strip_language_part=False)->str:
    """Generate an URL.
    """

    parsed_url = urlparse(url_str)

    # Absolute URL given, return it immediately
    if parsed_url[0]:
        return url_str

    # Defaults
    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
    r = [
        scheme(),  # 0, Scheme
        server_name(),  # 1, Netloc
        '',  # 2, Path
        '',  # 3, Params
        '',  # 4, Query
        '',  # 5, Fragment
    ]

    for k, v in enumerate(parsed_url):
        if parsed_url[k]:
            r[k] = parsed_url[k]

    if not strip_language_part:
        r[2] = str(base_path(language) + parsed_url[2]).replace('//', '/')

    return urlunparse(r)


def current_url(strip_query_string=False):
    """Get current URL.
    """
    r = request.url
    if strip_query_string:
        r = urlparse(r)
        r = urlunparse((r[0], r[1], r[2], r[3], '', ''))

    return r


def endpoint_url(endpoint: str, args: dict=None)->str:
    """Get URL for endpoint.
    """
    global __url_adapter
    try:
        return __url_adapter.build(endpoint, args)
    except BuildError:
        raise Exception("Cannot build URL for endpoint '{0}'.".format(endpoint))