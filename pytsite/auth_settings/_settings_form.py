"""PytSite Auth Settings Form
"""
from pytsite import settings as _settings, widget as _widget, lang as _lang, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    """PytSite Auth Settings Form
    """

    def _on_setup_widgets(self):
        self.add_widget(_widget.select.Checkbox(
            weight=10,
            uid='setting_signup_enabled',
            label=_lang.t('pytsite.auth_settings@allow_sign_up'),
        ))

        auth_driver_items = [(driver.name, driver.description) for driver in _auth.get_auth_drivers().values()]

        self.add_widget(_widget.select.Select(
            weight=20,
            uid='setting_auth_driver',
            append_none_item=False,
            label=_lang.t('pytsite.auth_settings@default_authentication_driver'),
            h_size='col-xs-12 col-sm-6 col-md-3',
            items=sorted(auth_driver_items, key=lambda i: i[0]),
            default=_auth.get_auth_driver().name,
        ))

        super()._on_setup_widgets()
