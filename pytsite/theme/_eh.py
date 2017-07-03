"""PytSite Theme Event Handlers
"""
from pytsite import settings as _settings, file as _file, assetman as _assetman, \
    metatag as _metatag
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    if not _assetman.is_package_registered(_api.get().package_name):
        return

    # Set favicon URL
    favicon_fid = _settings.get('theme.favicon_fid')
    if favicon_fid:
        try:
            f = _file.get(favicon_fid)
            _metatag.rm('link', rel='icon')
            _metatag.t_set('link', rel='icon', type=f.mime, href=f.get_url(width=50, height=50))
        except _file.error.FileNotFound:
            pass
    else:
        _metatag.t_set('link', rel='icon', type='image/png', href=_assetman.url('$theme@img/favicon.png'))
