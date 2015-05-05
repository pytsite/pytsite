from pytsite.core.view import *


def test(args: dict, request: Request):
    return render_tpl('app', 'test.jinja2', {'a': 'hello'})


