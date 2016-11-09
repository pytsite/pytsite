"""PytSite Mail Settings Form.
"""
from pytsite import widget as _widget, lang as _lang, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    def _setup_widgets(self):
        self.add_widget(_widget.input.Email(
            uid='setting_from',
            weight=10,
            label=_lang.t('pytsite.mail@default_sender_address'),
            required=True,
        ))

        super()._setup_widgets()
