"""Taxonomy Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


import re
from pytsite.core import router, lang
from pytsite.core.util import transform_str_1
from pytsite.core.odm import odm_manager, I_DESC
from pytsite.core.odm.finder import ODMFinder
from pytsite.admin import sidebar
from .models import AbstractTerm

__models = []


def register_model(model: str, cls: type, menu_weight: int=0, menu_icon: str='fa fa-tags'):
    """Register taxonomy model.
    """
    if not issubclass(cls, AbstractTerm):
        raise TypeError('Subclass of AbstractTerm expected.')

    if is_model_registered(model):
        raise Exception("Model '{}' is already registered as taxonomy model.". format(model))

    odm_manager.register_model(model, cls)
    __models.append(model)

    mock = odm_manager.dispense(model)
    """:type: pytsite.taxonomy.models.AbstractTerm"""

    menu_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    sidebar.add_menu('taxonomy', model, mock.t_plural(model), menu_url, menu_icon, weight=menu_weight,
                     permissions=('pytsite.odm_ui.browse.' + model,))


def is_model_registered(model: str) -> bool:
    """Check if the model is registered as taxonomy model.
    """
    return model in __models


def find(model: str) -> ODMFinder:
    """Get finder for the taxonomy model.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as taxonomy model.". format(model))

    return odm_manager.find(model).where('language', '=', lang.get_current_lang()).sort([('weight', I_DESC)])


def sanitize_alias_string(model: str, string: str) -> str:
    """Sanitize a path string.
    """
    string = transform_str_1(string)

    itr = 0
    while True:
        if not find(model).where('alias', '=', string).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub(r'-\d+$', '-' + str(itr), string)
