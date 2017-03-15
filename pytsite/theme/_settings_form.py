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
        for theme in _api.get_all().values():
            self.add_widget(_widget.input.Hidden(
                uid='setting_theme_' + theme.name,
                form_area='hidden',
            ))

        self.add_widget(_widget.select.Select(
            uid='setting_default_theme',
            weight=10,
            label=_lang.t('pytsite.theme@default_theme'),
            required=True,
            items=sorted([(pkg_name, theme.description) for pkg_name, theme in _api.get_all().items()]),
            h_size='col-xs-12 col-sm-6 col-md-5 col-lg-4',
            default=_api.get().package_name,
            assets=['pytsite.theme@js/settings-form.js'],
            append_none_item=False,
        ))

        # Logo
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_logo_fid',
            weight=10,
            label=_lang.t('pytsite.theme@logo'),
        ))

        # Favicon
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_favicon_fid',
            weight=20,
            label=_lang.t('pytsite.theme@favicon'),
        ))

        try:
            super()._on_setup_widgets()
        except _file.error.FileNotFound:
            pass

    def _on_submit(self):
        """Hook.
        """
        # First, process settings form to store values
        r = super()._on_submit()

        # Current theme
        default_theme_package = self.values.get('setting_default_theme')

        # Rebuild assets for selected theme
        _assetman.build(default_theme_package, cache=False)

        # Set default theme
        _api.set_default(_api.get(default_theme_package))

        return r

