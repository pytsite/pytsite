"""PytSite Auth UI Event Handlers
"""
from datetime import datetime as _datetime
from pytsite import auth as _auth, router as _router, lang as _lang, reg as _reg, http as _http, hreflang as _hreflang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch Event Handler
    """
    # User is anonymous by default
    user = _auth.get_anonymous_user()

    # Determine current user based on session's data
    if 'pytsite.auth.login' in _router.session():
        try:
            session = _router.session()
            user = _auth.get_user(session['pytsite.auth.login'])
            session.modified = True  # Update session's timestamp
        except _auth.error.UserNotExist:
            # User has been deleted, so delete session information about it
            del _router.session()['pytsite.auth.login']

    # Set current user
    _auth.switch_user(user)

    if not user.is_anonymous:
        if user.status == 'active':
            # Disable page caching for signed in users
            _router.set_no_cache(True)

            # Update user's activity timestamp
            user.last_activity = _datetime.now()
            user.save()
        else:
            # Sign out inactive user
            _auth.sign_out(user)

    # Alternate languages for sign in page
    if len(_lang.langs()) > 1:
        base_path = _reg.get('auth.base_path', '/auth/login')
        if base_path == _router.current_path(True):
            for lng in _lang.langs(False):
                _hreflang.add(lng, _router.url(base_path, lang=lng))


def router_response(response: _http.response.Response):
    # If user signed out, but session cookie is still alive
    if 'PYTSITE_SESSION' in _router.request().cookies and _auth.get_current_user().is_anonymous:
        try:
            _router.delete_session(_router.session())
        except KeyError:
            pass

        response.delete_cookie('PYTSITE_SESSION')
