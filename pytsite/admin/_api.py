"""Admin API Functions
"""
from pytsite import tpl as _tpl, widget as _widget, core_version_str as _version_str, core_url as _core_url, \
    core_name as _core_name, form as _form, assetman as _assetman, auth as _auth, http as _http, reg as _reg, \
    router as _router
from . import _sidebar

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def base_path() -> str:
    return _reg.get('admin.base_path', '/admin')


def render(content: str) -> str:
    """Render admin page with content.
    """
    if not _auth.get_current_user().has_permission('pytsite.admin.use'):
        raise _http.error.Forbidden()

    return _tpl.render('pytsite.admin@html', {
        'admin_sidebar': _sidebar.render(),
        'admin_language_nav': _widget.select.LanguageNav('admin-language-nav', dropdown=True),
        'content': content,
        'core_name': _core_name,
        'core_url': _core_url,
        'core_version': _version_str(),
        'sidebar_collapsed': _router.request().cookies.get('adminSidebarCollapsed') is not None
    })


def render_form(frm: _form.Form) -> str:
    """Render a form on the admin page.
    """
    _assetman.add('pytsite.admin@css/admin-form.css')
    frm.css += ' admin-form'

    return render(_tpl.render('pytsite.admin@form', {'form': frm}))
