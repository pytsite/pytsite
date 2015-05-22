"""ODM UI Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.lang import t
from pytsite.core import tpl
from pytsite.core.http.response import RedirectResponse
from pytsite.core.odm import odm_manager
from pytsite.core.widget.button import SubmitButtonWidget
from pytsite.core.widget.wrapper import WrapperWidget
from . import odm_ui_manager
from .browser import ODMUIBrowser
from .model import ODMUIForm


def browse(args: dict, inp: dict) -> str:
    return tpl.render('pytsite.odm_ui@admin_browser', {'browser': ODMUIBrowser(args.get('model'))})


def get_modify_form(args: dict, inp: dict) -> str:
    entity = odm_manager.dispense(args.get('model'), args.get('id'))
    ui = odm_ui_manager.dispense(args.get('model'), entity)

    form = ODMUIForm('odm-ui-form')
    actions_wrapper = WrapperWidget()
    actions_wrapper.add_child(SubmitButtonWidget(value=t('pytsite.odm_ui@save'), color='primary', icon='fa fa-save'))
    form.add_widget(actions_wrapper)

    ui.setup_modify_form(entity, form)

    return tpl.render('pytsite.odm_ui@admin_modify_form', {'form': form})


def post_modify_form(args: dict, inp: dict) -> RedirectResponse:
    pass
