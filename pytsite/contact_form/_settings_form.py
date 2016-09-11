"""PytSite AddThis Settings Form.
"""
from pytsite import widget as _widget, lang as _lang, settings as _settings, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    def _setup_widgets(self):
        self.add_widget(_widget.input.StringList(
            uid='setting_recipients',
            weight=10,
            label=_lang.t('pytsite.contact_form@recipient_emails'),
            required=True,
            rules=_validation.rule.Email(),
            add_btn_label=_lang.t('pytsite.contact_form@add_recipient'),
        ))

        super()._setup_widgets()
