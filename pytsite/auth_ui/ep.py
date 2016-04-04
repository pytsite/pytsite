"""Auth UI Endpoints
"""
from pytsite import auth as _auth, odm_ui as _odm_ui, reg as _reg, http as _http, metatag as _metatag, tpl as _tpl, \
    router as _router
from . import _widget as _auth_ui_widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def profile_view(args: dict, inp: dict) -> str:
    """Profile view endpoint.
    """
    tpl_name = 'pytsite.auth_ui@profile-view'
    current_user = _auth.get_current_user()
    profile_owner = _auth.get_user(nickname=args.get('nickname'))
    """:type: pytsite.auth_ui._model.UserUI"""

    # Profile owner does nto exist
    if not profile_owner:
        raise _http.error.NotFound()

    # Non-public profiles cannot be viewed by anonymous users
    if current_user.is_anonymous and not profile_owner.profile_is_public:
        raise _http.error.NotFound()

    # Non public profiles can be viewed only by administrators
    if not current_user.is_admin and current_user.id != profile_owner.id and not profile_owner.profile_is_public:
        raise _http.error.NotFound()

    _metatag.t_set('title', profile_owner.full_name)

    # Give control of the response to an alternate endpoint
    target_ep = _reg.get('auth_ui.ep.profile_view')
    if target_ep and _router.is_ep_callable(target_ep):
        args.update({
            'tpl': tpl_name,
            'user': profile_owner
        })
        return _router.call_ep(target_ep, args, inp)

    # Default response
    return _tpl.render(tpl_name, {
        'profile_widget': _auth_ui_widget.Profile('auth-ui-profile-widget', user=profile_owner),
        'follow_widget': _auth_ui_widget.Follow(uid='auth-ui-follow-widget', user=profile_owner),
    })


def profile_edit(args: dict, inp: dict) -> str:
    """Profile edit endpoint.
    """
    # Check if the profile owner is exists
    profile_owner = _auth.get_user(nickname=args.get('nickname'))
    if not profile_owner:
        raise _http.error.NotFound()

    tpl_name = 'pytsite.auth_ui@profile-edit'
    frm = _odm_ui.get_m_form('user', str(profile_owner.id), uid='auth-ui-profile')

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


def follow(args: dict, inp: dict) -> dict:
    """Follow widget JS endpoint.
    """
    op = inp.get('op')
    uid = inp.get('uid')

    # Does all required arguments present?
    if not op or not uid:
        return {'status': False}

    # Is current user authorized
    current_user = _auth.get_current_user()
    if current_user.is_anonymous:
        return {'status': False}

    user = _auth.get_user(uid=inp.get('uid'))

    if op == 'follow':
        user.f_add('followers', current_user).save()
        current_user.f_add('follows', user).save()
        return {'status': True}
    elif op == 'unfollow':
        user.f_sub('followers', current_user).save()
        current_user.f_sub('follows', user).save()
        return {'status': True}
    else:
        return {'status': False}
