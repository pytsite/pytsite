"""pytsite.lang Errors
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class LanguageNotSupported(Exception):
    pass


class PackageNotRegistered(Exception):
    pass


class TranslationError(Exception):
    pass
