from werkzeug.routing import Map as __Map

__routes = __Map()
__url_adapter = None


def add_rule(pattern: str, endpoint: str, defaults: dict=None, methods=None, redirect_to: str=None):
    """Add a rule to the router.
    """
    from werkzeug.routing import Rule

    rule = Rule(
        string=pattern,
        endpoint=endpoint,
        defaults=defaults,
        methods=methods,
        redirect_to=redirect_to
    )

    __routes.add(rule)


def dispatch(env: dict, start_response: callable):
    """Dispatch the request.
    """
    from werkzeug.exceptions import HTTPException, NotFound
    from werkzeug.wrappers import Request, Response
    from werkzeug.utils import redirect
    from importlib import import_module
    from re import sub

    global __url_adapter
    __url_adapter = __routes.bind_to_environ(env)

    path_info = __url_adapter.path_info

    # Remove trailing slash
    if len(path_info) > 1 and path_info.endswith('/'):
        redirect_url = sub(r'/$', '', path_info)
        if __url_adapter.query_args:
            redirect_url += '?' + __url_adapter.query_args
        return redirect(redirect_url, 301)(env, start_response)

    try:
        endpoint_str, values = __url_adapter.match()

        endpoint = endpoint_str.split('::')
        if len(endpoint) != 2:
            raise TypeError("Invalid format of endpoint specification: '{0}'".format(endpoint))

        module_name, callable_name = endpoint[0], endpoint[1]
        try:
            module = import_module(module_name)
            if callable_name not in dir(module):
                raise Exception("Callable specified in endpoint '{0}' doesn't exists .".format(endpoint))

            callable_obj = getattr(module, callable_name)
            if not hasattr(callable_obj, '__call__'):
                raise Exception("'{0}' is not callable".format(callable_name))

            # Call endpoint
            response = Response(response='', status=200, content_type='text/html')
            response_from_callable = callable_obj(values, request=Request(env))
            if isinstance(response_from_callable, str):
                response.data = response_from_callable
            elif isinstance(response_from_callable, Response):
                response = response_from_callable
            else:
                response.data = ''

            return response(env, start_response)

        except ImportError as e:
            e.msg = "Cannot load module '{0}' specified in endpoint '{1}': {2}.".format(module_name, endpoint, e.msg)
            raise e

    except HTTPException as e:
        return e(env, start_response)


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
    from . import registry
    name = registry.get_val('console.server_name', 'localhost')
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
    from urllib.parse import urlparse, urlunparse

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
