"""PytSite Base Settings Form.
"""
from pytsite import form as _form, router as _router, widget as _widget, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class SettingsForm(_form.Form):
    def __init__(self, uid: str = None, **kwargs):
        self._setting_uid = kwargs.get('setting_uid')

        super().__init__(uid, **kwargs)

    def _setup_form(self):
        self._action = _router.ep_url('pytsite.settings.ep.form_submit', {'uid': self._setting_uid})

    def _setup_widgets(self):
        from ._api import get_definition, get_setting

        setting_def = get_definition(self._setting_uid)
        setting_def['form_widgets_setup'](self, get_setting(self._setting_uid))

        self.data.update({
            'setting-uid': self._setting_uid
        })

        self.add_widget(_widget.button.Link(
            uid='action-cancel',
            weight=10,
            value=_lang.t('pytsite.settings@cancel'),
            icon='fa fa-ban',
            href=_router.ep_url('pytsite.admin.ep.dashboard'),
            form_area='footer'
        ))
