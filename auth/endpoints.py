__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.utils import escape
from pytsite.core import view, metatag, lang, router
from . import manager


def get_login(args: dict, inp: dict)->str:
    """Get login form.
    """
    print(inp)
    metatag.set_tag('title', lang.t('pytsite.auth@authorization'))
    return view.render_tpl('pytsite.auth@views/login', {'form': manager.get_login_form()})


def post_login(args: dict, inp: dict)->router.RedirectResponse:
    """Process login form submit.
    """
    return manager.post_login_form(args, inp)


def filter_authorize(args: dict, inp: dict)->router.RedirectResponse:
    inp['redirect'] = escape(router.current_url(True))
    redirect_url = router.endpoint_url('pytsite.auth.endpoints.get_login', inp)

    return router.RedirectResponse(redirect_url)