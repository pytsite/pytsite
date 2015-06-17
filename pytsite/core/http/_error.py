__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug import exceptions as _e


class NotFoundError(_e.NotFound):
    pass


class ForbiddenError(_e.Forbidden):
    pass


class InternalServerError(_e.InternalServerError):
    pass
