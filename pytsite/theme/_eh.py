"""PytSite Theme Event Handlers
"""
from typing import Optional as _Optional
from pytsite import settings as _settings, file as _file, assetman as _assetman, metatag as _metatag, odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    if not _assetman.is_package_registered(_api.get().package_name):
        return

    # Set current theme package
    _metatag.t_set('pytsite-theme', _api.get().package_name)

    # Set favicon URL
    favicon_fid = _settings.get('theme.favicon')
    if favicon_fid:
        try:
            f = _file.get(favicon_fid)
            _metatag.t_set('link', rel='icon', type=f.mime, href=f.get_url(width=50, height=50))
        except _file.error.FileNotFound:
            pass
    else:
        _metatag.t_set('link', rel='icon', type='image/png', href=_assetman.url('$theme@img/favicon.png'))


def lang_translate(language: str, package_name: str, msg_id: str) -> _Optional[str]:
    """pytsite.lang.translate
    """
    if package_name == _api.get().package_name:
        e = _odm.find('theme_translation') \
            .eq('language', language) \
            .eq('message_id', '{}@{}'.format(package_name, msg_id)) \
            .first()

        return e.f_get('translation') if e else None

    return None
