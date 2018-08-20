from werkzeug import exceptions as _e

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Base(_e.HTTPException):
    pass


class E4xx(Base):
    pass


class NotFound(E4xx, _e.NotFound):
    pass


class Unauthorized(E4xx, _e.Unauthorized):
    pass


class Forbidden(E4xx, _e.Forbidden):
    pass


class MethodNotAllowed(E4xx, _e.MethodNotAllowed):
    pass


class E5xx(Base):
    pass


class InternalServerError(E5xx, _e.InternalServerError):
    pass
