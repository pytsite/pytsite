"""PytSite Base Settings Form.
"""
from pytsite import form as _form, router as _router, widget as _widget, lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_form.Form):
    """Base settings form.
    """

    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        self._setting_uid = kwargs.get('setting_uid')

        super().__init__(uid, **kwargs)

        self._data.update({
            'setting-uid': self._setting_uid
        })

    def _setup_form(self, **kwargs):
        """Hook.
        """
        self._action = _router.ep_url('pytsite.settings@form_submit', {'uid': self._setting_uid})

    def _setup_widgets(self):
        # Fill form widgets with values
        for k, v in _api.get(self._setting_uid).items():
            try:
                self.get_widget('setting_' + k).value = v
            except _form.error.WidgetNotFound:
                pass

        self.add_widget(_widget.button.Link(
            uid='action-cancel',
            weight=10,
            value=_lang.t('pytsite.settings@cancel'),
            icon='fa fa-fw fa-ban',
            href=_router.ep_url('pytsite.admin@dashboard'),
            form_area='footer'
        ))
