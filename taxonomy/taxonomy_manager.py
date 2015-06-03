"""Taxonomy Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core import router
from pytsite.core.odm import odm_manager
from pytsite.admin import sidebar
from .models import AbstractTerm


def register_model(model: str, cls: type, menu_weight: int=0, menu_icon: str='fa fa-tags'):
    """Register taxonomy model.
    """

    if not issubclass(cls, AbstractTerm):
        raise TypeError('Subclass of AbstractTerm expected.')

    odm_manager.register_model(model, cls)

    mock = odm_manager.dispense(model)
    """:type: pytsite.taxonomy.models.AbstractTerm"""

    menu_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    sidebar.add_menu('taxonomy', model, mock.t_plural(model), menu_url, menu_icon, weight=menu_weight,
                     permissions=('pytsite.odm_ui.browse.' + model,))
