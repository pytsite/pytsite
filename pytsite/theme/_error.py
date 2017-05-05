"""PytSite Theme Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ThemeInitError(Exception):
    pass


class ThemeLoadError(Exception):
    pass


class NoThemesRegistered(Exception):
    def __str__(self):
        return 'No themes registered'


class ThemeNotRegistered(Exception):
    def __init__(self, name: str):
        self._theme_name = name

    def __str__(self):
        return "Theme '{}' is not registered".format(self._theme_name)


class ThemeAlreadyRegistered(Exception):
    def __init__(self, name: str):
        self._theme_name = name

    def __str__(self):
        return "Theme '{}' is already registered".format(self._theme_name)
