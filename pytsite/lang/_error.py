"""pytsite.lang Errors
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class LanguageNotSupported(Error):
    pass


class PackageNotRegistered(Error):
    pass


class PackageAlreadyRegistered(Error):
    pass


class TranslationError(Error):
    pass
