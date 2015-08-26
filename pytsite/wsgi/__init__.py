"""PytSite WSGI Dispatcher Entry Point.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import setup, router

# Check if the setup completed
if not setup.is_setup_completed():
    raise Exception('Setup is not completed.')

# Public API
application = router.dispatch
