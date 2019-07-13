"""PytSite Mail API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router, reg


def mail_from() -> tuple:
    """Get default mail sender's address and name.
    """
    return reg.get('mail.from', 'info@' + router.server_name())
