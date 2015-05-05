from werkzeug.routing import Map as __Map

__routes = __Map()


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
    from importlib import import_module

    adapter = __routes.bind_to_environ(env)
    try:
        endpoint_str, values = adapter.match()

        endpoint = endpoint_str.split('::')
        if len(endpoint) != 2:
            raise TypeError("Invalid format in endpoint specification: '{0}'".format(endpoint))

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