"""PytSite AddThis Settings Form.
"""
from pytsite import widget as _widget, lang as _lang, settings as _settings, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    def _setup_widgets(self):
        self.add_widget(_widget.input.Text(
            uid='setting_pub_id',
            weight=10,
            label=_lang.t('pytsite.addthis@pub_id'),
            required=True,
            help=_lang.t('pytsite.addthis@pub_id_setup_help'),
            rules=_validation.rule.Regex(pattern='ra-[0-9a-f]{16}')
        ))

        super()._setup_widgets()
