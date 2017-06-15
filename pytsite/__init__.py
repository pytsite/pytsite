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
    import sys
    from importlib import import_module
    from os import path, environ, getcwd, mkdir, makedirs
    from getpass import getuser
    from socket import gethostname
    from . import reg

    # Environment type and name
    reg.put('env.type', 'uwsgi' if 'UWSGI_ORIGINAL_PROC_NAME' in environ else 'console')
    reg.put('env.name', getuser() + '@' + gethostname())

    # Workaround for some cases
    if '/usr/local/bin' not in environ['PATH'] and path.exists('/usr/local/bin'):
        environ['PATH'] += ':/usr/local/bin'

    # Detecting app's root path
    cwd = getcwd()
    pd = path.abspath(path.join(cwd, path.pardir))
    if path.isdir(path.join(cwd, 'env')):
        root_path = cwd
    elif path.isdir(path.join(pd, 'env')):
        root_path = pd
    else:
        raise FileNotFoundError('Cannot locate virtualenv directory')

    # It is important for correct importing of packages inside 'themes', 'plugins', etc
    sys.path.append(root_path)

    # Base filesystem paths
    virtualenv_path = path.join(root_path, 'env')
    app_path = path.join(root_path, 'app')
    reg.put('paths.root', root_path)
    reg.put('paths.virtualenv', virtualenv_path)
    reg.put('paths.app', app_path)
    for n in ['config', 'log', 'static', 'storage', 'tmp']:
        reg.put('paths.' + n, path.join(root_path, n))

    # PytSite path
    reg.put('paths.pytsite', path.join(root_path, path.dirname(__file__)))

    # Create cache directory
    reg.put('paths.cache', path.join(reg.get('paths.tmp'), 'cache'))
    makedirs(reg.get('paths.cache'), 0o755, True)

    # uWSGI does not export virtualenv paths, do it by ourselves
    if 'VIRTUAL_ENV' not in environ:
        environ['VIRTUAL_ENV'] = virtualenv_path
        environ['PATH'] = path.join(virtualenv_path, 'bin') + ':' + environ['PATH']

    # Additional filesystem paths
    reg.put('paths.session', path.join(reg.get('paths.tmp'), 'session'))
    reg.put('paths.setup.lock', path.join(reg.get('paths.storage'), 'setup.lock'))
    reg.put('paths.maintenance.lock', path.join(reg.get('paths.storage'), 'maintenance.lock'))

    # Create 'app' package
    if not path.exists(app_path):
        mkdir(app_path, 0o755)
        with open(path.join(app_path, '__init__.py'), 'w') as f:
            f.write('"""PytSite Application.\n"""\n')

        # Create default configuration file
        config_dir = reg.get('paths.config')
        if not path.exists(config_dir):
            mkdir(config_dir, 0o755)
            conf_str = 'server_name: test.com\n' \
                       '# db:\n' \
                       '  # database: test_com\n' \
                       '  # user: test\n' \
                       '  # password: test\n' \
                       '  # ssl: true\n'
            with open(path.join(config_dir, 'default.yml'), 'w') as f:
                f.write(conf_str)

    # Debug is disabled by default
    reg.put('debug', False)

    # Switching registry to the file driver
    file_driver = reg.driver.File(reg.get('paths.config'), reg.get('env.name'))
    reg.set_driver(file_driver)

    # Default output parameters
    reg.put('output', {
        'minify': not reg.get('debug'),
    })

    # Initialize required core packages. Order is important.
    autoload = ('theme', 'cron', 'stats', 'auth_storage_odm', 'reload', 'update', 'setup', 'cleanup', 'odm_http_api',
                'browser', 'plugman', 'testing')
    for pkg_name in autoload:
        import_module('pytsite.' + pkg_name)

    # Initialize authentication subsystem
    import_module('pytsite.auth_password')
    import_module('pytsite.auth_ulogin')

    # Create application's language directory
    from pytsite import lang
    app_lng_dir = path.join(app_path, 'lang')
    if not path.exists(app_lng_dir):
        mkdir(app_lng_dir, 0o755)
        for lng in lang.langs():
            with open(path.join(app_lng_dir, '{}.yml'.format(lng)), 'w') as f:
                f.write('')

    # Initialize 'app' package
    lang.register_package('app', 'lang')
    import_module('app')

    # Core event handlers
    from pytsite import events
    from . import _eh
    events.listen('pytsite.update', _eh.update)

    # Load theme
    from pytsite import theme
    theme.load()


_init()
