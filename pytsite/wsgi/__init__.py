"""PytSite WSGI Dispatcher Entry Point.
"""
from pytsite import router as _router

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Public API
application = _router.dispatch
