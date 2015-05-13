"""PytSite Application.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from importlib import import_module
from pytsite.core import reg, router


def dispatch(env, start_response):
    """WSGI dispatch.
    """
    return router.dispatch(env, start_response)

# Autoload modules
for module_name in reg.get_val('autoload', []):
    import_module(module_name)
