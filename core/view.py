from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import NotFound, Forbidden


def render_tpl(package: str, tpl_name: str, data: dict=None)->str:
    from .tpl import render
    if data is None:
        data = dict()
    return render(package, tpl_name, data)


def json_response(data: dict)->Response:
    import json
    return Response(json.dumps(data), content_type='application/json')


def redirect_response(loc: str, code=302)->Response:
    from werkzeug.utils import redirect
    return redirect(loc, code)


def not_found():
    raise NotFound()


def forbidden():
    raise Forbidden
