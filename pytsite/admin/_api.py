"""Admin API Functions
"""
from pytsite import tpl as _tpl, widget as _widget, core_version_str as _version_str, core_url as _core_url, \
    core_name as _core_name, form as _form, assetman as _assetman
from . import _sidebar

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def render(content: str) -> str:
    """Render admin page with content.
    """
    return _tpl.render('pytsite.admin@html', {
        'admin_sidebar': _sidebar.render(),
        'admin_language_nav': _widget.select.LanguageNav('admin-language-nav', dropdown=True),
        'content': content,
        'core_name': _core_name,
        'core_url': _core_url,
        'core_version': _version_str(),
    })


def render_form(frm: _form.Form) -> str:
    """Render a form on the admin page.
    """
    _assetman.add('pytsite.admin@css/admin-form.css')
    frm.css += ' admin-form'

    return render(_tpl.render('pytsite.admin@form', {'form': frm}))
