__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug import exceptions as _e


class NotFound(_e.NotFound):
    pass


class Forbidden(_e.Forbidden):
    pass


class InternalServerError(_e.InternalServerError):
    pass
