"""PytSite Auth UI AJAX Endpoints.
"""
from pytsite import auth as _auth, events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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
        _events.fire('pytsite.auth_ui.follow', user=user, follower=current_user)

        return {'status': True}
    elif op == 'unfollow':
        user.f_sub('followers', current_user).save()
        current_user.f_sub('follows', user).save()
        _events.fire('pytsite.auth_ui.unfollow', user=user, follower=current_user)

        return {'status': True}
    else:
        return {'status': False}
