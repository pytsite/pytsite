__initialized = False
__logger = None


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


def is_initialized()->bool:
    """Check whether the application is initialized.
    """
    return __initialized


def init(caller_file: str):
    """Init.
    """
    import getpass
    import socket
    from os import path
    from . import registry

    # Logger
    import logging
    global __logger
    __logger = logging.getLogger()

    # Environment
    registry.set_val('env.name', getpass.getuser() + '@' + socket.gethostname())

    # Filesystem paths
    root_path = path.abspath(path.dirname(caller_file))
    app_path = path.join(root_path, 'app')
    static_path = path.join(root_path, 'static')
    registry.set_val('paths.root', root_path)
    registry.set_val('paths.app', app_path)
    registry.set_val('paths.static', static_path)
    for n in ['config', 'log', 'storage', 'tmp', 'themes']:
        registry.set_val('paths.' + n, path.join(app_path, n))

    # Output parameters
    registry.set_val('output', {
        'minify': False,
        'theme': 'default',
        'compress_css': False,
        'compress_js': False,
    })

    # Debug parameters
    registry.set_val('debug', {'enabled': False})

    # Switching registry to the file driver
    file_driver = registry.FileDriver(registry.get_val('paths.config'), registry.get_val('env.name'))
    registry.set_driver(file_driver)

    from . import lang

    # Available languages
    lang.define_languages(registry.get_val('lang.languages', ['en']))

    # Core's languages store
    lang.register_package('pytsite.core')

    from . import tpl

    # Core's templates store
    tpl.register_package('pytsite.core')

    from importlib import import_module

    # Autoloading modules
    for module_name in registry.get_val('autoload', []):
        import_module(module_name)

    # Initializing 'app' package
    import_module('app')

    # App's languages storage
    lang.register_package('app')

    from . import assetman

    # App's templates and assets storage
    theme = registry.get_val('output.theme')
    templates_dir = 'themes' + path.sep + theme + path.sep + 'tpl'
    tpl.register_package('app', templates_dir)
    assets_dir = 'themes' + path.sep + theme + path.sep + 'assets'
    assetman.register_package('app', assets_dir)

    # Loading routes from the registry
    __load_routes_from_registry()

    global __initialized
    __initialized = True


def logger():
    """Get application logger.
    """
    return __logger


def wsgi(env, start_response):
    """Call application via WSGI.
    """
    if not __initialized:
        raise Exception("Application is not initialized.")

    from .router import dispatch
    return dispatch(env, start_response)


def run():
    """Run application in console mode.
    """
    if not __initialized:
        raise Exception("Application is not initialized.")

    from . import console
    console.run()