"""Admin API Functions
"""
from pytsite import tpl as _tpl, widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def render(content: str) -> str:
    """Render admin page with content.
    """
    return _tpl.render('pytsite.admin@html', {
        'admin_language_nav': _widget.select.LanguageNav('admin-language-nav', dropdown=True),
        'content': content,
    })
