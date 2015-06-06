__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug import exceptions


class NotFoundError(exceptions.NotFound):
    pass


class ForbiddenError(exceptions.Forbidden):
    pass


class InternalServerError(exceptions.InternalServerError):
    pass
