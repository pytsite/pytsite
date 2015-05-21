"""ODM UI Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import tpl
from pytsite.core.http.response import RedirectResponse
from pytsite.core.http.errors import Forbidden
from pytsite.auth import auth_manager
from .browser import ODMBrowser


def browse(args: dict, inp: dict) -> str:
    return tpl.render('pytsite.admin@html', {'content': ODMBrowser(args.get('model')).render()})


def get_form(args: dict, inp: dict) -> str:
    pass


def post_form(args: dict, inp: dict) -> RedirectResponse:
    pass


def js_api_get_browser_rows(args: dict, inp: dict) -> list:
    model = inp.get('model')
    if not model:
        raise Exception('Model is not specified')

    if not auth_manager.get_current_user().has_permission('pytsite.odm_ui.browse.{}'.format(model)):
        raise Forbidden()

    return []
