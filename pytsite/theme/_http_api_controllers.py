"""PytSite Theme HTTP API.
"""
from pytsite import auth as _auth, routing as _routing
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class GetSettings(_routing.Controller):
    def exec(self):
        if not _auth.get_current_user().has_permission('pytsite.theme.manage'):
            raise self.forbidden()

        r = []

        try:
            theme = _api.get(self.arg('theme_name'))

            for w in theme.package.get_settings_widgets():
                setting_val = theme.settings.get(w.uid)
                if setting_val:
                    w.value = setting_val

                w.uid = 'setting_theme_{}_{}'.format(theme.name, w.uid).replace('.', '_')
                w.name = 'setting_theme_{}[{}]'.format(theme.name, w.name)

                r.append(w.render())

        except AttributeError:
            # Theme may not define get_settings_widget()
            pass

        return r
