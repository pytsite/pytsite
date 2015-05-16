__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.utils import escape
from pytsite.core import view, metatag, lang, router
from . import manager


def get_login(args: dict, inp: dict)->str:
    """Get login form.
    """
    metatag.set_tag('title', lang.t('pytsite.auth@authorization'))
    return view.render_tpl('pytsite.auth@views/login', {'form': manager.get_login_form()})


def post_login(args: dict, inp: dict) -> router.RedirectResponse:
    """Process login form submit.
    """

    return manager.post_login_form(args, inp)


def get_logout(args: dict, inp: dict) -> router.RedirectResponse:
    """Logout endpoint.
    """

    manager.logout_current_user()
    redirect_url = router.base_url()
    if 'redirect' in inp:
        redirect_url = router.url(inp['redirect'])
    return router.RedirectResponse(redirect_url)


def filter_authorize(args: dict, inp: dict) -> router.RedirectResponse:
    """Authorization filter.
    """

    # User is currently authorized, nothing to do
    if manager.get_current_user():
        return None

    # Redirecting to the authorization endpoint
    inp['redirect'] = escape(router.current_url(True))
    return router.RedirectResponse(router.endpoint_url('pytsite.auth.endpoints.get_login', inp))
