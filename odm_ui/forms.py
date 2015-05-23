"""ODM UI Forms.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router
from pytsite.core.form import AbstractForm
from pytsite.core.widget.wrapper import WrapperWidget
from pytsite.core.widget.button import SubmitButtonWidget, LinkButtonWidget
from . import odm_ui_manager


class ODMUIForm(AbstractForm):
    """ODM UI Form.
    """

    def __init__(self, uid, model: str, entity: ODMModel=None, **kwargs: dict):
        super().__init__(uid, **kwargs)

        self._model = model

    def _setup(self):
        """Hook.
        """

        actions_wrapper = WrapperWidget()
        submit_button = SubmitButtonWidget(value=t('pytsite.odm_ui@save'), color='primary', icon='fa fa-save')
        cancel_button_url = router.endpoint_url('pytsite.odm_ui.endpoints.browse', {'model': self._model})
        cancel_button = LinkButtonWidget(value=t('pytsite.odm_ui@cancel'), href=cancel_button_url, icon='fa fa-ban')
        actions_wrapper.add_child(submit_button, 10).add_child(cancel_button, 20)
        self.add_widget(actions_wrapper)