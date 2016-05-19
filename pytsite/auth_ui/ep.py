"""Auth UI Endpoints
"""
from pytsite import auth as _auth, odm_ui as _odm_ui, reg as _reg, http as _http, metatag as _metatag, tpl as _tpl, \
    router as _router, lang as _lang
from . import _widget as _auth_ui_widget, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def profile_view(args: dict, inp: dict) -> str:
    """Profile view endpoint.
    """
    current_user = _auth.get_current_user()
    profile_owner = _auth.get_user(nickname=args.get('nickname')) # type: _model.UserUI

    if _tpl.tpl_exists('app@auth_ui/profile-view'):
        tpl_name = 'app@auth_ui/profile-view'
    else:
        tpl_name = 'pytsite.auth_ui@profile-view'

    # Profile owner does nto exist
    if not profile_owner:
        raise _http.error.NotFound()

    # Non-public profiles cannot be viewed by anonymous users
    if current_user.is_anonymous and not profile_owner.profile_is_public:
        raise _http.error.NotFound()

    # Non public profiles can be viewed only by administrators
    if not current_user.is_admin and current_user.id != profile_owner.id and not profile_owner.profile_is_public:
        raise _http.error.NotFound()

    # Page title
    _metatag.t_set('title', profile_owner.full_name)

    # Widgets
    profile_widget = _auth_ui_widget.Profile('auth-ui-profile-widget', user=profile_owner)

    # Alternative response handler
    if _router.is_ep_callable('$theme.ep.auth_ui_profile_view'):
        args.update({
            'tpl': tpl_name,
            'user': profile_owner,
            'profile_widget': profile_widget,
        })

        return _router.call_ep('$theme.ep.auth_ui_profile_view', args, inp)

    # Default response
    return _tpl.render(tpl_name, {
        'profile_widget': profile_widget,
    })


def profile_edit(args: dict, inp: dict) -> str:
    """Profile edit endpoint.
    """
    # Check if the profile owner is exists
    profile_owner = _auth.get_user(nickname=args.get('nickname'))
    if not profile_owner:
        raise _http.error.NotFound()

    tpl_name = 'pytsite.auth_ui@profile-edit'
    frm = _odm_ui.get_m_form('user', str(profile_owner.id))
    frm.title = _lang.t('pytsite.auth_ui@profile_edit')
    _metatag.t_set('title', _lang.t('pytsite.auth_ui@profile_edit'))

    # Give control of the response to an alternate endpoint
    target_ep = _reg.get('auth_ui.ep.profile_edit')
    if target_ep and _router.is_ep_callable(target_ep):
        args.update({
            'tpl': tpl_name,
            'user': profile_owner,
            'frm': frm,
        })
        return _router.call_ep(target_ep, args, inp)

    # Default response
    return _tpl.render(tpl_name, {'frm': frm})
