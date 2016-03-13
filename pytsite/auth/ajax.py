"""PytSite Auth AJAX Endpoints.
"""
from pytsite import assetman as _assetman, reg as _reg, util as _util
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_login_form(args: dict, inp: dict) -> dict:
    frm = _api.get_login_form(
        inp.get('driver'),
        inp.get('title'),
        inp.get('uid'),
        inp.get('css', ''),
        inp.get('modal', False)
    )

    return {
        'form': _util.minify_html(frm.render()),
        '_css': _assetman.get_urls('css'),
        '_js': _assetman.get_urls('js')
    }


def is_anonymous(args: dict, inp: dict) -> bool:
    return _api.get_current_user().is_anonymous
