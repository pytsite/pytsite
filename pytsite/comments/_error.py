"""PytSite Comments Package Errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class DriverAlreadyRegistered(Exception):
    pass


class DriverNotRegistered(Exception):
    pass


class InvalidCommentStatus(Exception):
    pass


class CommentNotExist(Exception):
    pass


class CommentTooShort(Exception):
    pass


class CommentTooLong(Exception):
    pass
