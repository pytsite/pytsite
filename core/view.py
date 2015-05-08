from werkzeug.wrappers import Response


def render_tpl(tpl_location: str, data: dict=None)->str:
    """Render template.
    """
    from . import tpl
    return tpl.render(tpl_location, data)


def json_response(data: dict)->Response:
    """Make JSON response.
    """
    import json
    return Response(json.dumps(data), content_type='application/json')


def redirect_response(loc: str, code=302)->Response:
    """Make redirect response.
    """
    from werkzeug.utils import redirect
    return redirect(loc, code)


def not_found():
    """Raise HTTP 'Not Found' exception.
    """
    from werkzeug.exceptions import NotFound
    raise NotFound()


def forbidden():
    """Raise HTTP 'Forbidden' exception.
    """
    from werkzeug.exceptions import Forbidden
    raise Forbidden()
