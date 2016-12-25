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
    from os import path, environ, getcwd, mkdir
    from getpass import getuser
    from socket import gethostname
    from . import reg

    # Environment type and name
    reg.put('env.type', 'uwsgi' if 'UWSGI_ORIGINAL_PROC_NAME' in environ else 'console')
    reg.put('env.name', getuser() + '@' + gethostname())

    # Workaround for some cases
    if '/usr/local/bin' not in environ['PATH'] and path.exists('/usr/local/bin'):
        environ['PATH'] += ':/usr/local/bin'

    # Base filesystem paths
    root_path = getcwd()
    app_path = path.join(root_path, 'app')
    reg.put('paths.root', root_path)
    reg.put('paths.app', app_path)
    for n in ['config', 'log', 'static', 'storage', 'tmp']:
        reg.put('paths.' + n, path.join(root_path, n))

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
    autoload = ('theme', 'cron', 'reload', 'update', 'setup', 'cleanup', 'auth_password', 'auth_ulogin',
                'odm_http_api', 'plugman')
    for pkg_name in autoload:
        import_module('pytsite.' + pkg_name)

    # Create application's language directory
    from pytsite import lang
    app_lng_dir = path.join(app_path, 'lang')
    if not path.exists(app_lng_dir):
        mkdir(app_lng_dir, 0o755)
        for lng in lang.langs():
            with open(path.join(app_lng_dir, '{}.yml'.format(lng)), 'w') as f:
                f.write('')

    # Register application's language directory
    lang.register_package('app', 'lang')

    # Initialize 'app' package
    import_module('app')

    # Core event handlers
    from pytsite import events
    from . import _eh
    events.listen('pytsite.update', _eh.update)


_init()
