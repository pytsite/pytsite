"""Admin API Functions
"""
from pytsite import tpl as _tpl, widget as _widget, core_version_str as _version_str, core_url as _core_url, \
    core_name as _core_name, browser as _browser, assetman as _assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def render(content: str) -> str:
    """Render admin page with content.
    """
    _browser.include('bootstrap') 
    _browser.include('font-awesome')
    _assetman.add('pytsite.admin@AdminLTE/css/AdminLTE.min.css')
    _assetman.add('pytsite.admin@AdminLTE/css/skins/skin-blue.min.css')
    _assetman.add('pytsite.admin@css/custom.css')
    _assetman.add('pytsite.admin@AdminLTE/js/app.js')
    
    return _tpl.render('pytsite.admin@html', {
        'admin_language_nav': _widget.select.LanguageNav('admin-language-nav', dropdown=True),
        'content': content,
        'core_name': _core_name,
        'core_url': _core_url,
        'core_version': _version_str(),
    })
