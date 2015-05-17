"""PytSite Core Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from getpass import getuser
from socket import gethostname
from importlib import import_module
from os import path, environ
from .core import reg

if 'PYTSITE_APP_ROOT' not in environ:
    raise Exception("The 'PYTSITE_APP_ROOT' environment variable is not defined.")

# Environment
reg.set_val('env.name', getuser() + '@' + gethostname())

# Filesystem paths
root_path = path.abspath(environ['PYTSITE_APP_ROOT'])
if not path.exists(root_path) or not path.isdir(root_path):
    raise Exception("{0} is not exists or it is not a directory.")
app_path = path.join(root_path, 'app')
static_path = path.join(root_path, 'static')
reg.set_val('paths.root', root_path)
reg.set_val('paths.app', app_path)
reg.set_val('paths.static', static_path)
for n in ['config', 'log', 'storage', 'tmp', 'themes']:
    reg.set_val('paths.' + n, path.join(app_path, n))
reg.set_val('paths.session', path.join(reg.get_val('paths.tmp'), 'session'))

# Output parameters
reg.set_val('output', {
    'minify': True,
    'theme': 'default',
    'compress_css': False,
    'compress_js': False,
    'base_tpl': 'app@html',
})

# Debug parameters
reg.set_val('debug', {'enabled': False})

# Switching registry to the file driver
file_driver = reg.FileDriver(reg.get_val('paths.config'), reg.get_val('env.name'))
reg.set_driver(file_driver)

# Now it is possible to initialize language subsystem
from pytsite.core import lang
lang.define_languages(reg.get_val('lang.languages', ['en']))
lang.register_package('pytsite.core', 'resources/lang')

# Now it possible to initialize template engine
from pytsite.core import tpl
tpl.register_package('pytsite.core', 'resources/tpl')

# Initializing event subsystem
from pytsite.core import events

# Initialize console
from pytsite.core import console
from pytsite.core.commands.cleanup import *
console.register_command(CleanupSessionCommand())
console.register_command(CleanupTmpCommand())
console.register_command(CleanupAllCommand())

# Initializing cron
from pytsite.core import cron
cron.register_console_commands()

# Initializing 'app' package
import_module('app')
lang.register_package('app')

# Initializing asset manager
from pytsite.core import assetman
theme = reg.get_val('output.theme')
templates_dir = 'themes' + path.sep + theme + path.sep + 'tpl'
tpl.register_package('app', templates_dir)
assets_dir = 'themes' + path.sep + theme + path.sep + 'assets'
assetman.register_package('app', assets_dir)

# Initializing router
from .core import router

# Loading routes from the registry
for pattern, opts in reg.get_val('routes', {}).items():
    if '_endpoint' not in opts and '_redirect' not in opts:
        raise Exception("'_endpoint' or '_redirect' is not defined for route '{0}'".format(pattern))

    endpoint = None
    if '_endpoint' in opts:
        endpoint = opts['_endpoint']

    redirect = None
    if '_redirect' in opts:
        redirect = opts['_redirect']

    defaults = {}
    for k, v in opts.items():
        if not v.startswith('_'):
            defaults[k] = v

    methods = ('GET', 'POST')
    if '_methods' in opts:
        methods = opts['_methods']

    router.add_rule(pattern, endpoint, defaults, methods, redirect)
