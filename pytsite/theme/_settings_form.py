"""PytSite Theme Settings Form.
"""
from collections import OrderedDict as _OrderedDict
from pytsite import widget as _widget, lang as _lang, settings as _settings, assetman as _assetman, file as _file
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):

    @property
    def values(self) -> _OrderedDict:
        v = super().values

        for k in 'setting_logo_fid', 'setting_favicon_fid':
            v[k] = v[k][0].uid if v[k] else None

        return v

    def _on_setup_widgets(self):
        for t_info in _api.get_list().values():
            self.add_widget(_widget.input.Hidden(
                uid='setting_theme_' + t_info['name'],
                form_area='hidden',
            ))

        self.add_widget(_widget.select.Select(
            uid='setting_default_theme',
            weight=10,
            label=_lang.t('pytsite.theme@default_theme'),
            required=True,
            items=sorted([(k, v['description']) for k, v in _api.get_list().items()]),
            h_size='col-xs-12 col-sm-6 col-md-5 col-lg-4',
            default=_api.get_current(),
            assets=['pytsite.theme@js/settings-form.js'],
            append_none_item=False,
        ))

        # Logo
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_logo_fid',
            weight=10,
            label=_lang.t('pytsite.theme@logo'),
            show_numbers=False,
            dnd=False,
        ))

        # Favicon
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_favicon_fid',
            weight=20,
            label=_lang.t('pytsite.theme@favicon'),
            show_numbers=False,
            dnd=False,
        ))

        try:
            super()._on_setup_widgets()
        except _file.error.FileNotFound:
            pass

    def _on_submit(self):
        """Hook.
        """
        # Rebuild assets for selected theme
        _assetman.build(self.values.get('setting_default_theme'), cache=False)

        return super()._on_submit()
