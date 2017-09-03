"""PytSite Base Settings Form
"""
import re as _re
from pytsite import form as _form, router as _router, widget as _widget, lang as _lang, auth as _auth, http as _http, \
    util as _util, validation as _validation, events as _events
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_form.Form):
    """Base settings form
    """

    def __init__(self, **kwargs):
        """Init
        """
        self._setting_uid = kwargs.get('setting_uid')

        kwargs.update({
            'name': 'settings-' + self._setting_uid,
            'css': 'settings-form setting-uid-' + self._setting_uid,
        })

        super().__init__(**kwargs)

    def _on_setup_widgets(self):
        """Hook
        """
        _events.fire('pytsite.settings.form.setup_widgets', frm=self)
        _events.fire('pytsite.settings.form.setup_widgets.' + self._setting_uid, frm=self)

        # Fill form widgets with values
        for k, v in _api.get(self._setting_uid).items():
            try:
                self.get_widget('setting_' + k).value = v
            except _form.error.WidgetNotExist:
                pass

        self.add_widget(_widget.button.Link(
            uid='action-cancel-' + str(self.step),
            weight=10,
            value=_lang.t('pytsite.settings@cancel'),
            icon='fa fa-fw fa-ban',
            href=_router.rule_url('pytsite.admin@dashboard'),
            form_area='footer',
        ))

    def _on_submit(self):
        setting_uid = self._setting_uid

        user = _auth.get_current_user()
        setting_def = _api.get_definition(setting_uid)

        if setting_def['perm_name'] != '*' and not user.has_permission(setting_def['perm_name']):
            raise _http.error.Forbidden("Current user does not have permission '{}'".format(setting_def['perm_name']))

        # Extract all values who's name starts with 'setting_'
        setting_value = {}
        for k, v in self.values.items():
            if k.startswith('setting_'):
                k = _re.sub('^setting_', '', k)

                if isinstance(v, (list, tuple)):
                    v = _util.cleanup_list(v)

                if isinstance(v, dict):
                    v = _util.cleanup_dict(v)

                setting_value[k] = v

        # Update settings
        _api.put(setting_uid, _util.dict_merge(_api.get(setting_uid), setting_value))

        _router.session().add_success_message(_lang.t('pytsite.settings@settings_has_been_saved'))

        return _http.response.Redirect(_router.rule_url('pytsite.settings@form', {'uid': setting_uid}))


class Application(Form):
    """Basic application's settings form
    """

    def _on_setup_widgets(self):
        """Hook
        """
        # Application names
        w = 10
        for l in _lang.langs():
            self.add_widget(_widget.input.Text(
                uid='setting_app_name_' + l,
                weight=w,
                label=_lang.t('pytsite.settings@application_name', {'lang': _lang.lang_title(l)}, l),
                default=_lang.t('app@app_name'),
            ))
            w += 1

            self.add_widget(_widget.input.Text(
                uid='setting_home_title_' + l,
                label=_lang.t('pytsite.settings@home_page_title', {'lang': _lang.lang_title(l)}, l),
                weight=w,
            ))
            w += 1

            self.add_widget(_widget.input.Text(
                uid='setting_home_description_' + l,
                label=_lang.t('pytsite.settings@home_page_description', {'lang': _lang.lang_title(l)}, l),
                weight=w,
            ))
            w += 1

            self.add_widget(_widget.input.Tokens(
                uid='setting_home_keywords_' + l,
                label=_lang.t('pytsite.settings@home_page_keywords', {'lang': _lang.lang_title(l)}, l),
                weight=w,
            ))
            w += 1

        # Links
        self.add_widget(_widget.input.StringList(
            uid='setting_links',
            weight=200,
            label=_lang.t('pytsite.settings@links'),
            add_btn_label=_lang.t('pytsite.settings@add_link'),
            unique=True,
            rules=_validation.rule.UrlList(),
        ))

        # It is important to call super method AFTER
        super()._on_setup_widgets()
