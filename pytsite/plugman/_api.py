"""PytSite Package Manager API Functions.
"""
from os import listdir as _listdir, path as _path
from importlib import import_module as _import_module
from pytsite import reg as _reg, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_plugins = {}


def init():
    # Build list of plugins
    root = _reg.get('paths.plugins')
    for name in _listdir(root):
        abs_path = '{}{}{}'.format(root, _path.sep, name)
        if name in _plugins or not _path.isdir(abs_path) or name.startswith('__'):
            continue

        try:
            plugin = _import_module('app.plugins.' + name)

            for p in 'version', 'description', 'url':
                prop_name = '__pytsite_plugin_{}__'.format(p)
                if not hasattr(plugin, prop_name):
                    raise RuntimeError("Plugin '{}' must have '{}' property.".format(plugin.__name__, prop_name))

            if not hasattr(plugin, 'load') or not callable(plugin.load):
                raise RuntimeError("Plugin '{}' must have 'load()' function.".format(plugin.__name__))

            _plugins[name] = plugin

            if name in _settings.get('plugman.enabled_plugins', ()):
                plugin.load()

        except ImportError:
            raise RuntimeError("'{}' is not a python package.".format(abs_path))


def get_plugins():
    return _plugins
