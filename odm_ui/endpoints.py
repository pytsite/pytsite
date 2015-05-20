"""ODM UI Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import tpl
from pytsite.core.http.response import RedirectResponse
from .browser import ODMBrowser


def browse(args: dict, inp: dict) -> str:
    return tpl.render('pytsite.admin@html', {'content': ODMBrowser(args.get('model')).render()})


def get_form(args: dict, inp: dict) -> str:
    pass


def post_form(args: dict, inp: dict) -> RedirectResponse:
    pass
