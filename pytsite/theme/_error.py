"""PytSite Theme Engine Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ThemeRegistrationFailed(Exception):
    pass


class ThemeNotRegistered(Exception):
    pass


class NoThemesRegistered(Exception):
    pass
