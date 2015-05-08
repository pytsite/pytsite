__initialized = False
__plugins = {}


def __load_routes_from_registry():
    """Loads routes from the __registry.
    """
    from . import registry

    for pattern, opts in registry.get_val('routes', {}).items():
        if '_endpoint' not in opts and '_redirect' not in opts:
            raise Exception("'_endpoint' or '_redirect' is not defined for route '{0}'".format(pattern))

        endpoint = None
        if '_endpoint' in opts:
            endpoint = opts['_endpoint']

        redirect = None
        if '_redirect' in opts:
            redirect = opts['_redirect']

        defaults = dict()
        for k, v in opts.items():
            if not v.startswith('_'):
                defaults[k] = v

        methods = ('GET', 'POST')
        if '_methods' in opts:
            methods = opts['_methods']

        from . import router
        router.add_rule(pattern, endpoint, defaults, methods, redirect)


def init(caller_file: str):
    """Init.
    """
    import getpass
    import socket
    from os import path
    from . import registry, lang, tpl, assetman

    # Environment
    registry.set_val('env.name', getpass.getuser() + '@' + socket.gethostname())

    # Filesystem paths
    root_path = path.dirname(caller_file)
    app_path = path.join(root_path, 'app')
    registry.set_val('paths.root', root_path)
    registry.set_val('paths.app', app_path)
    for n in ['config', 'log', 'storage', 'tmp', 'themes']:
        registry.set_val('paths.' + n, path.join(app_path, n))

    # Output parameters
    registry.set_val('output', {
        'minify': False,
        'theme': 'default',
        'compress_css': False,
        'compress_js': False
    })

    # Switching registry to the file driver
    file_driver = registry.FileDriver(registry.get_val('paths.config'), registry.get_val('env.name'))
    registry.set_driver(file_driver)

    # App's languages storage
    lang.define_languages(registry.get_val('lang.languages', ['en']))
    lang.register_package('app')

    theme = registry.get_val('output.theme')

    # App's templates storage
    templates_dir = 'themes' + path.sep + theme + path.sep + 'tpl'
    tpl.register_package('app', templates_dir)

    # App's assets storage
    assets_dir = 'themes' + path.sep + theme + path.sep + 'assets'
    assetman.register_package('app', assets_dir)

    # Loading routes from the registry
    __load_routes_from_registry()

    global __initialized
    __initialized = True


def register_plugin(plugin):
    if not __initialized:
        raise Exception("Application is not initialized.")

    if plugin.__class__.__name__ != 'module':
        raise Exception('Only modules can be registered as plugins.')

    if not hasattr(plugin, 'get_name') or not hasattr(getattr(plugin, 'get_name'), '__call__'):
        raise Exception("Module {0} missing function get_name().".format(plugin))

    if not hasattr(plugin, 'start') or not hasattr(getattr(plugin, 'start'), '__call__'):
        raise Exception("Module {0} missing function start().".format(plugin))

    __plugins[plugin.get_name()] = plugin


def wsgi(env, start_response):
    """Call application via WSGI.
    """
    if not __initialized:
        raise Exception("Application is not initialized.")

    from .router import dispatch
    return dispatch(env, start_response)


def console(*args):
    """Call application from console.
    """
    if not __initialized:
        raise Exception("Application is not initialized.")
