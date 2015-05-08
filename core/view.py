__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound, Forbidden
from werkzeug.utils import redirect
import json
from . import tpl


def render_tpl(tpl_location: str, data: dict=None)->str:
    """Render template.
    """
    return tpl.render(tpl_location, data)


def json_response(data: dict)->Response:
    """Make JSON response.
    """
    return Response(json.dumps(data), content_type='application/json')


def redirect_response(loc: str, code=302)->Response:
    """Make redirect response.
    """
    return redirect(loc, code)


def not_found():
    """Raise HTTP 'Not Found' exception.
    """
    raise NotFound()


def forbidden():
    """Raise HTTP 'Forbidden' exception.
    """
    raise Forbidden()
