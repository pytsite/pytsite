"""Admin API Functions
"""
from pytsite import tpl as _tpl, widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def render(content: str) -> str:
    return _tpl.render('pytsite.admin@html', {
        'language_nav': _widget.select.LanguageNav('language-nav', dropdown=True),
        'content': content,
    })
