"""PytSite File Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class FileNotFound(Error):
    pass


class InvalidFileUidFormat(Error):
    pass
