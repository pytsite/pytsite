"""PytSite Init
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper
    """
    import sys
    from importlib import import_module
    from sys import argv, exit
    from os import path, environ
    from getpass import getuser
    from socket import gethostname
    from . import reg, package_info

    # Load regisrty memory driver
    reg.set_driver(reg.driver.Memory())

    # Environment type and name
    reg.put('env.name', getuser() + '@' + gethostname())
    if len(argv) > 1 and argv[1] == 'test':
        reg.put('env.type', 'testing')
    else:
        reg.put('env.type', 'uwsgi' if 'UWSGI_ORIGINAL_PROC_NAME' in environ else 'console')

    # Detect application's root directory path
    cur_dir = path.abspath(path.dirname(__file__))
    while True:
        if path.exists(path.join(cur_dir, 'app', 'app.json')):
            root_path = cur_dir
            break
        elif cur_dir != '/':
            cur_dir = path.abspath(path.join(cur_dir, path.pardir))
        else:
            raise RuntimeError('Cannot determine root directory of application')

    # It is important for correct importing of packages inside 'themes', 'plugins', etc
    sys.path.append(root_path)

    # Base filesystem paths
    env_path = environ.get('VIRTUAL_ENV', path.join(root_path, 'env'))
    app_path = path.join(root_path, 'app')
    reg.put('paths.root', root_path)
    reg.put('paths.env', env_path)
    reg.put('paths.app', app_path)
    for n in ['config', 'log', 'static', 'storage', 'tmp']:
        reg.put('paths.' + n, path.join(root_path, n))

    # PytSite path
    reg.put('paths.pytsite', path.join(root_path, path.dirname(__file__)))

    # uWSGI does not export virtualenv paths, do it by ourselves
    if 'VIRTUAL_ENV' not in environ:
        environ['VIRTUAL_ENV'] = env_path
        environ['PATH'] = path.join(env_path, 'bin') + ':' + environ['PATH']

    # Additional filesystem paths
    reg.put('paths.session', path.join(reg.get('paths.storage'), 'session'))
    reg.put('paths.maintenance_lock', path.join(reg.get('paths.storage'), 'maintenance.lock'))

    # Debug is disabled by default
    reg.put('debug', False)

    # Check for 'app' package
    if not path.exists(app_path):
        raise FileNotFoundError("Directory '{}' is not found".format(app_path))

    # Switch registry to the file driver
    file_driver = reg.driver.File(reg.get('paths.config'), reg.get('env.name'), reg.get_driver())
    reg.set_driver(file_driver)

    # Default output parameters
    reg.put('output', {
        'minify': not reg.get('debug'),
    })

    # Initialize logger
    from . import logger
    logger.info('')
    logger.info('---===[ PytSite-{} Started ]===---'.format(package_info.version('pytsite')))

    # Initialize rest of the system
    from pytsite import console
    try:
        # Initialize cache with default driver
        from pytsite import cache
        cache.set_driver(cache.driver.File())

        # Load required core packages, order is important
        for pkg_name in ('cron', 'stats', 'reload', 'update', 'plugman', 'testing'):
            import_module('pytsite.' + pkg_name)

        # Register app's language resources
        if path.exists(path.join(app_path, 'lang')):
            from pytsite import lang
            lang.register_package('app', 'lang')

        # Load 'app' package
        import_module('app')

    except Warning as e:
        console.print_warning(e)

    except Exception as e:
        console.print_error(e)
        if reg.get('debug'):
            raise e

        exit(1)


_init()
