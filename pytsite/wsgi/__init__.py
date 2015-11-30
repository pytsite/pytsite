"""PytSite WSGI Dispatcher Entry Point.
"""
from pytsite import setup as _setup, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Check if the setup completed
if not _setup.is_setup_completed():
    raise Exception('Setup is not completed.')

# Public API
application = _router.dispatch
