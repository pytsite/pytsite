from werkzeug import exceptions as _e

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class NotFound(_e.NotFound):
    pass


class Forbidden(_e.Forbidden):
    pass


class InternalServerError(_e.InternalServerError):
    pass


class MethodNotAllowed(_e.MethodNotAllowed):
    pass
