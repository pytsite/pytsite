"""Pytsite Auth Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.utils import escape as _escape
from pytsite.core import router as _router, lang as _lang, http as _http, metatag as _metatag, tpl as _tpl, \
    assetman as _assetman
from . import _functions


def get_login(args: dict, inp: dict) -> str:
    """Get login form.
    """
    if not _functions.get_current_user().is_anonymous:
        redirect_url = _router.base_url()
        if 'redirect' in inp:
            redirect_url = _router.url(inp['redirect'])
        return _http.response.Redirect(redirect_url)

    _assetman.add('pytsite.auth@css/common.css')
    _metatag.t_set('title', _lang.t('auth@authorization'))

    return _tpl.render('pytsite.auth@views/login', {
        'form': _functions.get_login_form(legend=_lang.t('auth@authorization'))
    })


def post_login(args: dict, inp: dict) -> _http.response.Redirect:
    """Process login form submit.
    """
    return _functions.post_login_form(args, inp)


def logout(args: dict, inp: dict) -> _http.response.Redirect:
    """Logout endpoint.
    """
    _functions.logout_current_user()
    redirect_url = _router.base_url()
    if 'redirect' in inp:
        redirect_url = _router.url(inp['redirect'])
    return _http.response.Redirect(redirect_url)


def filter_authorize(args: dict, inp: dict) -> _http.response.Redirect:
    """Authorization filter.
    """
    user = _functions.get_current_user()
    if not user.is_anonymous:
        # Checking requested permissions
        req_perms_str = args.get('permissions', '')
        if req_perms_str:
            for perm in req_perms_str.split(','):
                if not user.has_permission(perm.strip()):
                    raise _http.error.ForbiddenError()
        return  # All permissions has been checked successfully

    # Redirecting to the authorization endpoint
    inp['redirect'] = _escape(_router.current_url(True))

    if '__form_location' in inp:
        del inp['__form_location']
    if '__form_redirect' in inp:
        del inp['__form_redirect']

    return _http.response.Redirect(_router.endpoint_url('pytsite.auth.eps.get_login', inp))
