"""ODM UI Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.auth import auth_manager
from pytsite.core.odm import odm_manager
from pytsite.core.odm.model import ODMModel
from .models import ODMUIModel

__models = {}


def register_model(odm_model: str, odm_ui_class: type, permission_group: str, lang_package: str):
    """Register ODM UI model.
    """

    if odm_model in __models:
        raise KeyError("UI class for ODM model '{}' is already registered.".format(odm_model))

    if not issubclass(odm_ui_class, ODMUIModel):
        raise TypeError("Subclass of ODMUIModel expected.")

    for perm_name in 'create', 'browse', 'browse_own', 'modify', 'modify_own', 'delete', 'delete_own':
        perm_description = lang_package + '@odm_ui_permission_' + perm_name + '_' + odm_model
        perm_full_name = 'pytsite.odm_ui.' + perm_name + '.' + odm_model
        auth_manager.define_permission(perm_full_name, perm_description, permission_group)

    __models[odm_model] = odm_ui_class


def dispense_ui(odm_model: str, odm_entity: ODMModel=None) -> ODMUIModel:
    """Dispense an UI entity.
    """

    if odm_entity:
        if not isinstance(odm_entity, odm_manager.get_model_class(odm_model)):
            raise TypeError("ODM entity is instance of invalid class.")

    ui_class = _get_ui_class(odm_model)

    return ui_class()


def _get_ui_class(odm_model: str) -> type:
    """Get ODM UI class for ODM model.
    """

    if odm_model not in __models:
        raise KeyError("UI class for ODM model '{}' is not registered.".format(odm_model))

    return __models[odm_model]
