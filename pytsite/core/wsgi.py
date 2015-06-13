"""PytSite WSGI Dispatcher Entry Point.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from os import path
from pytsite.core import reg, router
from pytsite.core.lang import t


def dispatch(env, start_response):
    """WSGI dispatch.
    """
    return router.dispatch(env, start_response)

# Check if the setup completed
if not path.exists(reg.get('paths.setup.lock')):
    raise Exception(t('pytsite.core@setup_is_not_completed'))
