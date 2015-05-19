"""PytSite WSGI Dispatcher Entry Point.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from os import path
from importlib import import_module
from pytsite.core import reg, router


def dispatch(env, start_response):
    """WSGI dispatch.
    """
    return router.dispatch(env, start_response)

# Check if the setup completed
if not path.exists(reg.get('paths.setup.lock')):
    raise Exception('pytsite.core@setup_is_not_completed')

# Auto load modules
for module_name in reg.get('autoload', []):
    import_module(module_name)
