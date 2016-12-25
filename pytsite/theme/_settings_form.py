"""PytSite Theme Settings Form.
"""
from pytsite import widget as _widget, lang as _lang, settings as _settings, assetman as _assetman
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    def _setup_widgets(self):
        self.add_widget(_widget.select.Select(
            uid='setting_default_theme',
            weight=10,
            label=_lang.t('pytsite.theme@default_theme'),
            required=True,
            items=sorted([(k, v['name']) for k, v in _api.get_list().items()]),
            h_size='col-xs-12 col-sm-6 col-md-5 col-lg-4',
            default=_api.get_current(),
            assets=['pytsite.theme@js/settings-form.js'],
        ))

        super()._setup_widgets()

    def _on_submit(self):
        _assetman.build(self.values.get('setting_default_theme'), cache=False)
