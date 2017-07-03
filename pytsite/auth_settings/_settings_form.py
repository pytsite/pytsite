"""PytSite Auth Settings Form
"""
from pytsite import settings as _settings, widget as _widget, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    """PytSite Auth Settings Form
    """
    def _on_setup_widgets(self):
        self.add_widget(_widget.select.Checkbox(
            uid = 'setting_signup_enabled',
            label=_lang.t('pytsite.auth_settings@allow_sign_up'),
        ))

        super()._on_setup_widgets()
