__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ..core import view
from ..core.router import Request, Response
from . import manager


def get_login(args, request: Request)->str:
    """Get login form.
    """
    return view.render_tpl('pytsite.auth@views/login', {'form': manager.get_login_form()})


def post_login(args: dict, inp: dict)->Response:
    """Process login form submit.
    """
    return manager.post_login_form(args, inp)