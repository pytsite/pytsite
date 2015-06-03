__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug import exceptions


class NotFound(exceptions.NotFound):
    pass


class ForbiddenError(exceptions.Forbidden):
    pass


class ServerError(exceptions.InternalServerError):
    pass
