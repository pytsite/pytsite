"""PytSite Theme HTTP API.
"""
from pytsite import auth as _auth, http as _http, settings as _settings
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_settings(inp: dict, theme_package_name: str):
    if not _auth.get_current_user().has_permission('pytsite.theme.manage'):
        raise _http.error.Forbidden()

    r = []

    try:
        t_info = _api.get_info(theme_package_name)
        t_name = t_info['name']
        for w in t_info['package'].get_settings_widgets():
            setting_val = _settings.get('theme.theme_' + t_name, {}).get(w.uid)
            if setting_val:
                w.value = setting_val

            w.uid = 'setting_{}_{}'.format(t_name, w.uid).replace('.', '_')
            w.name = 'setting_theme_{}[{}]'.format(t_name, w.name)

            r.append(w.render())

    except AttributeError:
        # Theme may not define get_settings_widget()
        pass

    return r
