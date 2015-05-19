"""PytSite __main__ Module.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from importlib import import_module
from .core import console, reg

# Auto load modules
for module_name in reg.get('autoload', []):
    import_module(module_name)

console.run()
