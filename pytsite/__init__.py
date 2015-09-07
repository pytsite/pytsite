"""PytSite Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__version = None
""":type: tuple"""


def version():
    from os import path

    global __version
    if not __version:
        with open(path.join(path.dirname(__file__), 'VERSION.txt')) as f:
            __version = f.readline().replace('\n', '').split('.')
            if len(__version) == 2:
                __version.append(0)
            for k, v in enumerate(__version):
                __version[k] = int(__version[k])
            __version = tuple(__version)

    if __version[1] > 99:
        raise ValueError('Version minor cannot be greater 99.')
    if __version[2] > 9:
        raise ValueError('Version revision cannot be greater 9.')

    return __version


def __init():
    """Init wrapper to hide imports.
    """
    from os import path, environ
    from getpass import getuser
    from socket import gethostname
    from . import reg

    if 'PYTSITE_APP_ROOT' not in environ:
        raise Exception("The 'PYTSITE_APP_ROOT' environment variable is not defined.")

    # Environment
    reg.set_val('env.name', getuser() + '@' + gethostname())

    # Base filesystem paths
    root_path = path.abspath(environ['PYTSITE_APP_ROOT'])
    if not path.exists(root_path) or not path.isdir(root_path):
        raise Exception("{} is not exists or it is not a directory.".format(root_path))
    app_path = path.join(root_path, 'app')
    static_path = path.join(root_path, 'static')
    reg.set_val('paths.root', root_path)
    reg.set_val('paths.app', app_path)
    reg.set_val('paths.static', static_path)
    for n in ['config', 'log', 'storage', 'tmp', 'themes']:
        reg.set_val('paths.' + n, path.join(app_path, n))

    # Additional filesystem paths
    reg.set_val('paths.session', path.join(reg.get('paths.tmp'), 'session'))
    reg.set_val('paths.setup.lock', path.join(reg.get('paths.storage'), 'setup.lock'))
    reg.set_val('paths.maintenance.lock', path.join(reg.get('paths.storage'), 'maintenance.lock'))

    # Output parameters
    reg.set_val('output', {
        'minify': True,
        'theme': 'default',
        'base_tpl': 'app@html',
    })

    # Debug parameters
    reg.set_val('debug', {'enabled': False})

    # Switching registry to the file driver
    file_driver = reg.driver.File(reg.get('paths.config'), reg.get('env.name'))
    reg.set_driver(file_driver)

    # Initializing language subsystem
    from . import lang
    lang.define_languages(reg.get('lang.languages', ['ru']))

    # Initializing template subsystem
    from . import tpl

    # Initializing event subsystem
    from . import events

    # Initializing console
    __import__('pytsite.console')

    # Initializing router
    from . import router

    # Initializing metatag
    from . import metatag
    events.listen('pytsite.router.dispatch', metatag.reset)

    # Loading routes from the registry
    for url_path, opts in reg.get('routes', {}).items():
        name = opts.get('_name')
        call = opts.get('_call')
        methods = opts.get('_methods', 'GET')
        filters = opts.get('_filters', ())

        args = {}
        for k, v in opts.items():
            if not k.startswith('_'):
                args[k] = v

        router.add_rule(url_path, name=name, call=call, args=args, methods=methods, filters=filters)

    # Initializing asset manager
    from pytsite import assetman

    # Initializing Browser module
    __import__('pytsite.browser')

    # Initializing Form module
    __import__('pytsite.form')

    # Initializing Setup module
    __import__('pytsite.setup')

    # Initializing Cron
    __import__('pytsite.cron')

    # Initializing Cleanup package
    __import__('pytsite.cleanup')

    # Initializing 'app' package parts
    lang.register_package('app', 'lang')
    theme = reg.get('output.theme')
    tpl.register_package('app', 'themes' + path.sep + theme + path.sep + 'tpl')
    assetman.register_package('app', 'themes' + path.sep + theme + path.sep + 'assets')

    # Autoloading required modules
    for module in reg.get('app.autoload', ()):
        __import__(module)

    # Initializing the 'app' package
    __import__('app')


__init()
