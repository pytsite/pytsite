"""PytSite Theme Settings Form
"""
import re as _re
from pytsite import widget as _widget, lang as _lang, settings as _settings, file as _file, http_api as _http_api, \
    html as _html, router as _router, odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_TRANSLATION_MSG_ID_RE = _re.compile('^translation_[a-z0-9._@]+')


class _ThemesBrowser(_widget.Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._data['http-api-ep-switch'] = _http_api.endpoint('pytsite.theme@switch')
        self._data['http-api-ep-uninstall'] = _http_api.endpoint('pytsite.theme@uninstall')
        self._js_module = 'pytsite-theme-widget-themes-browser'

    def _get_element(self, **kwargs) -> _html.Element:
        cont = _html.TagLessElement()

        cont.append(_html.H2(_lang.t('pytsite.theme@installed_themes')))

        table = cont.append(_html.Table(css='table table-striped table-bordered table-hover'))

        t_head = table.append(_html.Tr())
        t_head.append(_html.Th(_lang.t('pytsite.theme@name')))
        t_head.append(_html.Th(_lang.t('pytsite.theme@version')))
        t_head.append(_html.Th(_lang.t('pytsite.theme@author')))
        t_head.append(_html.Th(_lang.t('pytsite.theme@url')))
        t_head.append(_html.Th(_lang.t('pytsite.theme@actions')))

        t_body = table.append(_html.TBody())
        for theme in _api.get_registered().values():
            tr = t_body.append(_html.Tr())
            tr.append(_html.Td(theme.name))
            tr.append(_html.Td(theme.version))
            tr.append(_html.Td(_html.A(theme.author['name'], href=theme.author['url'], target='_blank')))
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

        return cont


class _TranslationsEditTable(_widget.Abstract):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._css = 'translations-edit-table'
        self._js_module = 'pytsite-theme-widget-translations-edit'

    def _get_element(self):
        cont = _html.TagLessElement()

        # Header
        cont.append(_html.H2(_lang.t('pytsite.theme@theme_translations')))

        # Table
        table = cont.append(_html.Table(css='table table-striped table-bordered table-hover'))

        # Table header
        t_head = table.append(_html.THead())
        t_head_tr = t_head.append(_html.Tr())
        t_head_tr.append(_html.Th(_lang.t('pytsite.theme@message_id')))
        t_head_tr.append(_html.Th(_lang.t('pytsite.theme@message_translation')))

        # Table body
        t_body = table.append(_html.TBody())
        theme_pkg_name = _api.get().package_name
        for msg_id, msg_trans in _lang.get_package_translations(theme_pkg_name).items():
            if msg_id.startswith('setting_'):
                continue

            tr = t_body.append(_html.Tr())

            # Message ID
            tr.append(_html.Td(msg_id, css='msg-id'))

            # Translation
            entity = _odm.find('theme_translation') \
                .eq('message_id', '{}@{}'.format(theme_pkg_name, msg_id)) \
                .eq('language', _lang.get_current()) \
                .first()
            if entity:
                msg_trans = entity.f_get('translation')

            msg_trans_td = tr.append(_html.Td(css='msg-translation'))
            msg_trans_td.append(_html.Input(type='text', name='translation_{}@{}'.format(theme_pkg_name, msg_id),
                                            value=msg_trans, css='form-control'))

        return cont


class Form(_settings.Form):
    def _on_setup_form(self, **kwargs):
        self.nocache = True

    def _on_setup_widgets(self):
        # Upload theme header
        self.add_widget(_widget.static.HTML(
            uid='upload_header',
            weight=10,
            em=_html.H2(_lang.t('pytsite.theme@install_or_update_theme'))
        ))

        # Upload theme input
        self.add_widget(_widget.input.File(
            uid='file',
            weight=11,
            max_files=1,
            upload_endpoint=_http_api.endpoint('pytsite.theme@install'),
        ))

        # Themes browser
        self.add_widget(_ThemesBrowser(
            uid='themes',
            weight=20,
        ))

        self.add_widget(_widget.static.HTML(
            uid='theme_settings_header',
            weight=30,
            em=_html.H2(_lang.t('pytsite.theme@theme_settings')),
        ))

        # Logo
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_logo',
            weight=31,
            label=_lang.t('pytsite.theme@logo'),
        ))

        # Favicon
        self.add_widget(_file.widget.ImagesUpload(
            uid='setting_favicon',
            weight=40,
            label=_lang.t('pytsite.theme@favicon'),
        ))

        # Translations
        self.add_widget(_TranslationsEditTable(
            uid='translations',
            weight=500,
        ))

        try:
            super()._on_setup_widgets()
        except _file.error.FileNotFound:
            pass

    def _on_submit(self):
        orig_translations = _lang.get_package_translations(_api.get().package_name)

        for k, v in _router.request().inp.items():
            if not k.startswith('translation_'):
                continue

            msg_full_id = k.replace('translation_', '')
            msg_id = msg_full_id.split('@')[1]
            msg_trans = v.strip()

            if msg_id not in orig_translations:
                raise RuntimeError("Message ID '{}' is not found in package's translations".format(msg_id))

            # Create or dispense entity
            entity = _odm.find('theme_translation') \
                .eq('message_id', msg_full_id) \
                .eq('language', _lang.get_current()) \
                .first()
            if not entity:
                entity = _odm.dispense('theme_translation')

            if msg_trans:
                # New message is the same as in the package's file translations, so custom translation can be deleted
                if orig_translations[msg_id] == msg_trans:
                    if not entity.is_new:
                        try:
                            entity.delete()
                        except _odm.error.EntityDeleted:
                            # Entity was deleted by another instance
                            pass

                # Save custom translation
                else:
                    entity.f_set('message_id', msg_full_id).f_set('translation', msg_trans).save()

            # If no translation was provided, delete entity
            elif not entity.is_new:
                try:
                    entity.delete()
                except _odm.error.EntityDeleted:
                    # Entity was deleted by another instance
                    pass

        # Clear translations cache
        _lang.clear_cache()

        return super()._on_submit()
