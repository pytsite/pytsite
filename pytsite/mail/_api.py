"""PytSite Mail API.
"""
from pytsite import lang as _lang, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def mail_from() -> tuple:
    """Get default mail sender's address and name.
    """
    return _lang.t('app_name'), _settings.get('mail.from')
