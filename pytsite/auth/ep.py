"""Pytsite Auth Endpoints.
"""
from werkzeug.utils import escape as _escape
from pytsite import lang as _lang, http as _http, metatag as _metatag, tpl as _tpl, assetman as _assetman, \
    router as _router, logger as _logger
from . import _api, _error, _widget as _auth_widget

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
        return _tpl.render('pytsite.auth@sign-in', {
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
        _logger.error(str(e), exc_info=e)
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


def profile_view(args: dict, inp: dict) -> str:
    """Profile view endpoint.
    """
    try:
        profile_owner = _api.get_user(nickname=args.get('nickname'))
    except _error.UserNotExist:
        raise _http.error.NotFound()

    c_user = _api.get_current_user()

    if _tpl.tpl_exists('app@auth/profile-view'):
        tpl_name = 'app@auth/profile-view'
    else:
        tpl_name = 'pytsite.auth@profile-view'

    # Non-public profiles cannot be viewed
    if not profile_owner.profile_is_public and c_user.login != profile_owner.login and not c_user.is_admin:
        raise _http.error.NotFound()

    # Page title
    _metatag.t_set('title', profile_owner.full_name)

    # Widgets
    profile_widget = _auth_widget.Profile('auth-ui-profile-widget', user=profile_owner)

    args.update({
        'profile_is_editable': c_user == profile_owner or c_user.is_admin,
        'user': profile_owner,
        'profile_widget': profile_widget,
    })

    # Give control of the response to an alternate endpoint
    if _router.is_ep_callable('$theme@auth_profile_view'):
        args.update({
            'tpl': tpl_name,
        })

        return _router.call_ep('$theme@auth_profile_view', args, inp)

    # Default response
    return _tpl.render(tpl_name, args)


def profile_edit(args: dict, inp: dict) -> str:
    """Profile edit endpoint.
    """
    # Check if the profile owner is exists
    profile_owner = _api.get_user(nickname=args.get('nickname'))
    if not profile_owner:
        raise _http.error.NotFound()

    tpl_name = 'pytsite.auth@profile-edit'

    frm = _api.get_user_modify_form(profile_owner)
    frm.title = _lang.t('pytsite.auth@profile_edit')
    frm.redirect = profile_owner.profile_view_url

    _metatag.t_set('title', frm.title)

    # Give control of the response to an alternate endpoint
    if _router.is_ep_callable('$theme@auth_profile_edit'):
        args.update({
            'tpl': tpl_name,
            'user': profile_owner,
            'frm': frm,
        })
        return _router.call_ep('$theme@auth_profile_edit', args, inp)

    # Default response
    return _tpl.render(tpl_name, {'frm': frm})


def f_authorize(args: dict, inp: dict) -> _http.response.Redirect:
    """Authorization filter.
    """
    user = _api.get_current_user()

    # If user already authenticated, check its permissions
    if not user.is_anonymous:
        # Checking permissions if this is necessary
        req_perms_str = args.get('perms', '')
        if req_perms_str:
            for perm in req_perms_str.split(','):
                if not user.has_permission(perm.strip()):
                    raise _http.error.Forbidden()

        # All permissions has been checked successfully, simply do nothing
        return

    # Redirecting to the authorization endpoint
    inp['__redirect'] = _escape(_router.current_url(True))
    inp['driver'] = _api.get_auth_driver().name

    if '__form_location' in inp:
        del inp['__form_location']

    return _http.response.Redirect(_router.ep_url('pytsite.auth@sign_in', inp))
