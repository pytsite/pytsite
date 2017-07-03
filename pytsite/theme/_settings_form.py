"""PytSite Theme Settings Form
"""
from collections import OrderedDict as _OrderedDict
from pytsite import widget as _widget, lang as _lang, settings as _settings, file as _file, http_api as _http_api, \
    html as _html
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _ThemesBrowser(_widget.Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._data['http-api-ep-switch'] = _http_api.endpoint('pytsite.theme@switch')
        self._data['http-api-ep-uninstall'] = _http_api.endpoint('pytsite.theme@uninstall')
        self._js_module = 'pytsite-theme-widget-themes-browser'

    def _get_element(self, **kwargs) -> _html.Element:
        table = _html.Table(css='table table-striped table-bordered')

        header = _html.Tr()
        header.append(_html.Th(_lang.t('pytsite.theme@name')))
        header.append(_html.Th(_lang.t('pytsite.theme@version')))
        header.append(_html.Th(_lang.t('pytsite.theme@author')))
        header.append(_html.Th(_lang.t('pytsite.theme@url')))
        header.append(_html.Th(_lang.t('pytsite.theme@actions')))
        table.append(header)

        for theme in _api.get_registered().values():
            tr = _html.Tr()
            tr.append(_html.Td(theme.description))
            tr.append(_html.Td(theme.version))
            tr.append(_html.Td(theme.author))

            tr.append(_html.Td(_html.A(theme.url, href=theme.url, target='_blank')))

            actions = _html.TagLessElement(child_sep='&nbsp;')

            if _api.get().name != theme.name:
                # 'Switch' button
                btn_switch = _html.A(title=_lang.t('pytsite.theme@switch_to_this_theme'), href='#', role='button',
                                     css='btn btn-default btn-xs button-switch', data_package_name=theme.package_name)
                btn_switch.append(_html.I(css='fa fa-power-off'))
                actions.append(btn_switch)

                # 'Uninstall' button
                btn_delete = _html.A(title=_lang.t('pytsite.theme@uninstall_theme'), href='#', role='button',
                                     css='btn btn-danger btn-xs button-uninstall', data_package_name=theme.package_name)
                btn_delete.append(_html.I(css='fa fa-trash'))
                actions.append(btn_delete)

            tr.append(_html.Td(actions))

            table.append(tr)

        return table


class Form(_settings.Form):
    @property
    def values(self) -> _OrderedDict:
        v = super().values

        for k in 'setting_logo_fid', 'setting_favicon_fid':
            v[k] = v[k][0].uid if v[k] else None

        return v

    def _on_setup_form(self, **kwargs):
        self.nocache = True

    def _on_setup_widgets(self):
        self.add_widget(_ThemesBrowser(
            uid='themes',
            weight=10,
        ))

        # Upload theme
        self.add_widget(_widget.input.File(
            uid='file',
            weight=20,
            max_files=1,
            label=_lang.t('pytsite.theme@install_or_update_theme'),
            upload_endpoint=_http_api.endpoint('pytsite.theme@install')
        ))

        # Logo
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_logo_fid',
            weight=30,
            label=_lang.t('pytsite.theme@logo'),
        ))

        # Favicon
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_favicon_fid',
            weight=40,
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

        _api.switch(self.values.get('setting_current'))

        return r
