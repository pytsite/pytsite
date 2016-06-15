"""Pytsite Auth Endpoints.
"""
from werkzeug.utils import escape as _escape
from pytsite import lang as _lang, http as _http, metatag as _metatag, tpl as _tpl, assetman as _assetman, \
    router as _router, logger as _logger
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def sign_in(args: dict, inp: dict) -> str:
    """Page with login form.
    """
    # Redirect user if it already authorized
    if not _api.get_current_user().is_anonymous:
        redirect_url = _router.base_url()
        if 'redirect' in inp:
            redirect_url = _router.url(inp['redirect'])
        return _http.response.Redirect(redirect_url)

    _assetman.add('pytsite.auth@css/common.css')
    _metatag.t_set('title', _lang.t('pytsite.auth@authentication'))

    try:
        return _tpl.render('pytsite.auth@views/login', {
            'driver': args['driver'],
            'form': _api.get_sign_in_form(args.get('driver')),
        })
    except _error.DriverNotRegistered:
        raise _http.error.NotFound()


def sign_in_submit(args: dict, inp: dict) -> _http.response.Redirect:
    """Process login form submit.
    """
    for i in ('__form_steps', '__form_step'):
        if i in inp:
            del inp[i]

    driver = args.pop('driver')
    redirect = inp.pop('__redirect', _router.base_url())

    try:
        _api.sign_in(driver, inp)
        return _http.response.Redirect(redirect)

    except _error.AuthenticationError:
        _router.session().add_error(_lang.t('pytsite.auth@authentication_error'))
        return _http.response.Redirect(_router.ep_url('pytsite.auth@sign_in', args={
            'driver': driver,
            '__redirect': redirect,
        }))

    except Exception as e:
        _logger.error(e)
        _router.session().add_error(str(e))
        return _http.response.Redirect(_router.ep_url('pytsite.auth@sign_in', args={
            'driver': driver,
            '__redirect': redirect,
        }))


def sign_out(args: dict, inp: dict) -> _http.response.Redirect:
    """Logout endpoint.
    """
    _api.sign_out(_api.get_current_user())

    return _http.response.Redirect(inp.get('__redirect', _router.base_url()))


def filter_authorize(args: dict, inp: dict) -> _http.response.Redirect:
    """Authorization filter.
    """
    user = _api.get_current_user()
    if not user.is_anonymous:
        # Checking requested permissions
        req_perms_str = args.get('permissions', '')
        if req_perms_str:
            for perm in req_perms_str.split(','):
                if not user.has_permission(perm.strip()):
                    raise _http.error.Forbidden()
        return  # All permissions has been checked successfully

    # Redirecting to the authorization endpoint
    inp['__redirect'] = _escape(_router.current_url(True))
    inp['driver'] = _api.get_driver().name

    if '__form_location' in inp:
        del inp['__form_location']

    return _http.response.Redirect(_router.ep_url('pytsite.auth@sign_in', inp))
