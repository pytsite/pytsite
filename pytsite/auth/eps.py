__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.utils import escape
from pytsite.core import metatag, router, tpl, http, lang
from . import _manager


def get_login(args: dict, inp: dict) -> str:
    """Get login form.
    """
    if not _manager.get_current_user().is_anonymous():
        redirect_url = router.base_url()
        if 'redirect' in inp:
            redirect_url = router.url(inp['redirect'])
        return http.response.RedirectResponse(redirect_url)

    metatag.t_set('title', lang.t('pytsite.auth@authorization'))
    return tpl.render('pytsite.auth@views/login', {'form': _manager.get_login_form()})


def post_login(args: dict, inp: dict) -> router.RedirectResponse:
    """Process login form submit.
    """
    return _manager.post_login_form(args, inp)


def get_logout(args: dict, inp: dict) -> router.RedirectResponse:
    """Logout endpoint.
    """
    _manager.logout_current_user()
    redirect_url = router.base_url()
    if 'redirect' in inp:
        redirect_url = router.url(inp['redirect'])
    return router.RedirectResponse(redirect_url)


def filter_authorize(args: dict, inp: dict) -> router.RedirectResponse:
    """Authorization filter.
    """
    user = _manager.get_current_user()
    if not user.is_anonymous():
        # Checking requested permissions
        req_perms_str = args.get('permissions', '')
        if req_perms_str:
            for perm in req_perms_str.split(','):
                if not user.has_permission(perm.strip()):
                    raise http.error.ForbiddenError()
        return

    # Redirecting to the authorization endpoint
    inp['redirect'] = escape(router.current_url(True))

    if '__form_location' in inp:
        del inp['__form_location']
    if '__form_redirect' in inp:
        del inp['__form_redirect']

    return router.RedirectResponse(router.endpoint_url('pytsite.auth.eps.get_login', inp))
