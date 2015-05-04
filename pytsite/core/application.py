import inspect
import socket
import getpass
from os import path
from pytsite.core import registry
from flask import Flask

__flask_app = Flask(__name__)
__flask_app.debug = True

# Plugins
__plugins = {}

# Environment
registry.set_val('env.name', getpass.getuser() + '@' + socket.gethostname())

# Registering necessary paths
sep = str(path.sep)
root_path = path.dirname(inspect.getouterframes(inspect.currentframe())[1][1])
registry.set_val('paths.root', root_path)
registry.set_val('paths.config', root_path + sep + 'config')
registry.set_val('paths.log', root_path + sep + 'log')
registry.set_val('paths.tpl', root_path + sep + 'tpl')

# Switching to the file driver
file_driver = registry.FileDriver(registry.get_val('paths.config'), registry.get_val('env.name'))
registry.set_driver(file_driver)


def register_plugin(plugin):
    if plugin.__class__.__name__ != 'module':
        raise Exception('Only modules can be registered as plugins.')

    if not hasattr(plugin, 'get_name') or not hasattr(getattr(plugin, 'get_name'), '__call__'):
        raise Exception("Module {0} missing function get_name().".format(plugin))

    if not hasattr(plugin, 'start') or not hasattr(getattr(plugin, 'start'), '__call__'):
        raise Exception("Module {0} missing function start().".format(plugin))

    __plugins[plugin.get_name()] = plugin


def get_plugins()->dict:
    return __plugins


def add_route(pattern, name, view_func):
    """Add a route.
    """
    __flask_app.add_url_rule(pattern, name, view_func)


def wsgi(env, start_response):
    """WSGI proxy function.
    """
    return __flask_app.wsgi_app(env, start_response)

