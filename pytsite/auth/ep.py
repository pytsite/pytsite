"""Pytsite Auth Endpoints.
"""
from werkzeug.utils import escape as _escape
from pytsite import lang as _lang, http as _http, metatag as _metatag, tpl as _tpl, assetman as _assetman, \
    router as _router
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def login(args: dict, inp: dict) -> str:
    """Render login page.
    """
    if not _functions.get_current_user().is_anonymous:
        redirect_url = _router.base_url()
        if 'redirect' in inp:
            redirect_url = _router.url(inp['redirect'])
        return _http.response.Redirect(redirect_url)

    _assetman.add('pytsite.auth@css/common.css')
    _metatag.t_set('title', _lang.t('pytsite.auth@authorization'))

    return _tpl.render('pytsite.auth@views/login', {
        'form': _functions.get_login_form(title=_lang.t('pytsite.auth@authorization'))
    })


def login_submit(args: dict, inp: dict) -> _http.response.Redirect:
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
                    raise _http.error.Forbidden()
        return  # All permissions has been checked successfully

    # Redirecting to the authorization endpoint
    inp['redirect'] = _escape(_router.current_url(True))

    if '__form_location' in inp:
        del inp['__form_location']
    if '__form_redirect' in inp:
        del inp['__form_redirect']

    return _http.response.Redirect(_router.ep_url('pytsite.auth.ep.login', inp))
