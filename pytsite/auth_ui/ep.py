"""Auth UI Endpoints
"""
from pytsite import auth as _auth, odm_ui as _odm_ui, reg as _reg, http as _http, metatag as _metatag, tpl as _tpl

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def profile_view(args: dict, inp: dict) -> str:
    """Profile view endpoint.
    """
    tpl_name = _reg.get('auth_ui.tpl.profile_view', 'pytsite.auth_ui@profile_view')
    current_user = _auth.get_current_user()
    profile_owner = _auth.get_user(nickname=args.get('nickname'))
    """:type: pytsite.auth_ui._model.UserUI"""

    if not profile_owner:
        raise _http.error.NotFound()

    if current_user.is_anonymous and not profile_owner.profile_is_public:
        raise _http.error.NotFound()

    if not current_user.is_admin and current_user.id != profile_owner.id and not profile_owner.profile_is_public:
        raise _http.error.NotFound()

    _metatag.t_set('title', profile_owner.full_name)

    return _tpl.render(tpl_name, {'user': profile_owner})


def profile_edit(args: dict, inp: dict) -> str:
    """Profile edit endpoint.
    """
    profile_owner = _auth.get_user(nickname=args.get('nickname'))
    if not profile_owner:
        raise _http.error.NotFound()

    tpl_name = _reg.get('auth_ui.tpl.profile_edit', 'pytsite.auth_ui@profile_edit')
    form = _odm_ui.get_m_form('user', str(profile_owner.id))

    return _tpl.render(tpl_name, {'form': form})


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
