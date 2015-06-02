"""ODM UI Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.odm import odm_manager
from pytsite.auth import auth_manager
from .models import ODMUIMixin

__models = {}


def odm_register_model(model: str, cls: type):
    """Register UI model.
    """

    # Just for debugging purposes
    if model in __models:
        raise KeyError("Model '{}' is already registered.".format(model))

    # Checking inheritance
    mock = odm_manager.dispense(model)
    if not isinstance(mock, ODMUIMixin):
        return

    # Registering permission group if doesn't already registered
    perm_group = mock.get_permission_group()
    if not auth_manager.get_permission_group(perm_group[0]):
        auth_manager.define_permission_group(*perm_group)

    # Registering permissions
    for perm_name in 'create', 'browse', 'browse_own', 'modify', 'modify_own', 'delete', 'delete_own':
        perm_description = mock.get_lang_package() + '@odm_ui_permission_' + perm_name + '_' + model
        perm_full_name = 'pytsite.odm_ui.' + perm_name + '.' + model
        auth_manager.define_permission(perm_full_name, perm_description, mock.get_permission_group()[0])

    __models[model] = model
