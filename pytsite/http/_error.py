from werkzeug import exceptions as _e

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Base(_e.HTTPException):
    pass


class NotFound(Base, _e.NotFound):
    pass


class Unauthorized(Base, _e.Unauthorized):
    pass


class Forbidden(Base, _e.Forbidden):
    pass


class InternalServerError(Base, _e.InternalServerError):
    pass


class MethodNotAllowed(Base, _e.MethodNotAllowed):
    pass
