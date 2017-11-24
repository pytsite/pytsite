"""PytSite Mail API
"""
from pytsite import router as _router, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def mail_from() -> tuple:
    """Get default mail sender's address and name.
    """
    return _reg.get('mail.from', 'info@' + _router.server_name())
