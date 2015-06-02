"""Content Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core import router
from pytsite.core.odm import odm_manager
from pytsite.admin import sidebar
from .models import ContentModel


def register_model(model: str, cls: type, menu_weight: int=0, menu_icon: str='fa fa-file-text-o'):
    """Register content model.
    """
    if not issubclass(cls, ContentModel):
        raise TypeError('Subclass of ContentModel expected.')

    odm_manager.register_model(model, cls)

    mock = odm_manager.dispense(model)
    """:type: pytsite.odm_ui.models.ODMUIMixin"""

    menu_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    sidebar.add_section_menu('content', model, mock.t_plural(model), menu_url, menu_icon, weight=menu_weight)
