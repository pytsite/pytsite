"""PytSite Theme HTTP API.
"""
from pytsite import auth as _auth, http as _http, settings as _settings
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_settings_widgets(**kwargs):
    if not _auth.get_current_user().has_permission('pytsite.theme.manage'):
        raise _http.error.Forbidden()

    r = []

    theme = kwargs.get('theme')
    if not theme:
        raise RuntimeError('Theme name is not specified')

    try:
        pkg = _api.get_theme_info(kwargs.get('theme'))['package']
        for w in pkg.get_settings_widgets():
            setting_uid = 'theme_setting_{}_{}'.format(theme, w.uid).replace('.', '_')
            w.uid = 'setting_' + setting_uid

            setting_val = _settings.get('theme.' + setting_uid)
            if setting_val:
                w.value = setting_val

            r.append(w.render())

    except AttributeError:
        # Theme may not define get_settings_widget()
        pass

    return r
