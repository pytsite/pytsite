"""PytSite Core Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

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

# Output parameters
reg.set_val('output', {
    'minify': False,
    'theme': 'default',
    'base_tpl': 'app@html',
})

# Debug parameters
reg.set_val('debug', {'enabled': False})


# Switching registry to the file driver
file_driver = reg.FileDriver(reg.get('paths.config'), reg.get('env.name'))
reg.set_driver(file_driver)


# Initializing language subsystem
from . import lang
lang.define_languages(reg.get('lang.languages', ['en']))
lang.register_package('pytsite.core', 'resources/lang')


# Initializing template subsystem
from . import tpl


# Initializing event subsystem
from . import events


# Initializing console
__import__('pytsite.core.console')


# Initializing router
from . import router


# Loading routes from the registry
for pattern, opts in reg.get('routes', {}).items():
    if '_endpoint' not in opts and '_redirect' not in opts:
        raise Exception("'_endpoint' or '_redirect' is not defined for route '{0}'".format(pattern))

    endpoint = opts.get('_endpoint')
    redirect = opts.get('_redirect')
    methods = opts.get('_methods', ['GET'])
    filters = opts.get('_filters', [])

    defaults = {}
    for k, v in opts.items():
        if not k.startswith('_'):
            defaults[k] = v

    router.add_rule(pattern, endpoint, defaults, methods, redirect, filters)


# Initializing asset manager
from pytsite.core import assetman
assetman.register_package('pytsite.core', 'resources/assets')


# Initializing client components
__import__('pytsite.core.client')


# Initializing 'app' package
__import__('app')
lang.register_package('app')
theme = reg.get('output.theme')
tpl.register_package('app', 'themes' + path.sep + theme + path.sep + 'tpl')
assetman.register_package('app', 'themes' + path.sep + theme + path.sep + 'assets')
