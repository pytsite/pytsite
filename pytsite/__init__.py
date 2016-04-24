"""PytSite Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

core_name = 'PytSite'
core_url = 'https://github.com/pytsite/'
__version = None  # type: tuple


def core_version():
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
    if __version[2] > 99:
        raise ValueError('Version revision cannot be greater 99.')

    return __version


def core_version_str() -> str:
    v = core_version()
    return '{}.{}.{}'.format(v[0], v[1], v[2])


def __init():
    """Init wrapper.
    """
    from os import path, environ, getcwd
    from getpass import getuser
    from socket import gethostname
    from . import reg

    # Environment type
    reg.set_val('env.type', 'uwsgi' if 'UWSGI_ORIGINAL_PROC_NAME' in environ else 'console')

    # Environment name
    reg.set_val('env.name', getuser() + '@' + gethostname())

    # Detecting application directory path
    if 'PYTSITE_APP_ROOT' in environ:
        root_path = path.abspath(environ['PYTSITE_APP_ROOT'])
    elif path.exists(path.join(getcwd(), 'app')):
        root_path = getcwd()
    else:
        raise Exception('Cannot find application directory.')

    # Check root
    if not path.exists(root_path) or not path.isdir(root_path):
        raise Exception("{} is not exists or it is not a directory.".format(root_path))

    # Base filesystem paths
    app_path = path.join(root_path, 'app')
    reg.set_val('paths.root', root_path)
    reg.set_val('paths.app', app_path)
    reg.set_val('paths.static', path.join(root_path, 'static'))
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

    # Debug is disabled by default
    reg.set_val('debug', False)

    # Switching registry to the file driver
    file_driver = reg.driver.File(reg.get('paths.config'), reg.get('env.name'))
    reg.set_driver(file_driver)

    # Initializing language subsystem
    from . import lang
    lang.define(reg.get('lang.languages', ['en']))

    # Initializing template subsystem
    from . import tpl

    # Initializing event subsystem
    from . import events

    # Initializing cron
    __import__('pytsite.cron')

    # Initializing console
    __import__('pytsite.console')

    # Initializing router
    from . import router

    # Initializing asset manager
    from pytsite import assetman

    # Initializing metatag
    from . import metatag

    # Initializing hreflang
    from . import hreflang

    # Initializing minimal set of required packages
    __import__('pytsite.browser')
    __import__('pytsite.form')
    __import__('pytsite.setup')
    __import__('pytsite.cleanup')

    # Initializing automatically loaded required packages
    for module in reg.get('app.autoload', ()):
        __import__(module)

    # Initializing 'app' package parts
    theme = reg.get('output.theme')
    lang.register_package('app', 'lang')
    tpl.register_package('app', 'themes' + path.sep + theme + path.sep + 'tpl')
    assetman.register_package('app', 'themes' + path.sep + theme + path.sep + 'assets')
    __import__('app.themes.' + theme)

    # Settings favicon href
    reg.set_val('metatag.favicon.href', 'img/favicon.png')


__init()
