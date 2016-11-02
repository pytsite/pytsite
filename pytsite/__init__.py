"""PytSite Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

core_name = 'PytSite'
core_url = 'https://pytsite.xyz'
_version = None  # type: tuple


def core_version():
    from os import path

    global _version
    if not _version:
        with open(path.join(path.dirname(__file__), 'VERSION.txt')) as f:
            _version = f.readline().replace('\n', '').split('.')
            if len(_version) == 2:
                _version.append(0)
            for k, v in enumerate(_version):
                _version[k] = int(_version[k])
            _version = tuple(_version)

    if _version[1] > 99:
        raise ValueError('Version minor cannot be greater 99.')
    if _version[2] > 99:
        raise ValueError('Version revision cannot be greater 99.')

    return _version


def core_version_str() -> str:
    v = core_version()
    return '{}.{}.{}'.format(v[0], v[1], v[2])


def _init():
    """Init wrapper.
    """
    from importlib import import_module
    from os import path, environ, getcwd
    from getpass import getuser
    from socket import gethostname
    from . import reg

    # Environment type
    reg.put('env.type', 'uwsgi' if 'UWSGI_ORIGINAL_PROC_NAME' in environ else 'console')

    # Environment name
    reg.put('env.name', getuser() + '@' + gethostname())

    # Detecting application directory path
    if 'PYTSITE_APP_ROOT' in environ:
        root_path = path.abspath(environ['PYTSITE_APP_ROOT'])
    elif path.exists(path.join(getcwd(), 'app')):
        root_path = getcwd()
    else:
        raise RuntimeError('Cannot find application directory.')

    # Check root
    if not path.exists(root_path) or not path.isdir(root_path):
        raise RuntimeError("{} is not exists or it is not a directory.".format(root_path))

    # Base filesystem paths
    app_path = path.join(root_path, 'app')
    reg.put('paths.root', root_path)
    reg.put('paths.app', app_path)
    reg.put('paths.static', path.join(root_path, 'static'))
    for n in ['config', 'log', 'plugins', 'storage', 'tmp', 'themes']:
        reg.put('paths.' + n, path.join(app_path, n))

    # Additional filesystem paths
    reg.put('paths.session', path.join(reg.get('paths.tmp'), 'session'))
    reg.put('paths.setup.lock', path.join(reg.get('paths.storage'), 'setup.lock'))
    reg.put('paths.maintenance.lock', path.join(reg.get('paths.storage'), 'maintenance.lock'))

    # Output parameters
    reg.put('output', {
        'minify': True,
        'theme': 'default',
        'base_tpl': 'app@html',
    })

    # Debug is disabled by default
    reg.put('debug', False)

    # Switching registry to the file driver
    file_driver = reg.driver.File(reg.get('paths.config'), reg.get('env.name'))
    reg.set_driver(file_driver)

    # Initialize required core packages
    autoload = ('lang', 'tpl', 'events', 'cron', 'console', 'router', 'assetman', 'metatag', 'hreflang', 'browser',
                'form', 'setup', 'reload', 'update', 'cleanup', 'auth', 'odm_http_api')
    for pkg_name in autoload:
        import_module('pytsite.' + pkg_name)

    # Initializing automatically loaded required packages
    for module in reg.get('autoload', ()):
        __import__(module)

    # Initializing 'app' package parts
    from pytsite import lang, tpl, assetman
    theme = reg.get('output.theme')
    lang.register_package('app', 'lang')
    tpl.register_package('app', 'themes' + path.sep + theme + path.sep + 'tpl')
    assetman.register_package('app', 'themes' + path.sep + theme + path.sep + 'assets')
    __import__('app.themes.' + theme)

    # Initialize plugins
    __import__('pytsite.plugman')

    # Settings favicon href
    reg.put('metatag.favicon.href', 'img/favicon.png')


_init()
