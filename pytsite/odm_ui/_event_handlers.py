"""ODM UI Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang, odm
from pytsite.auth import _manager
from ._model import ODMUIMixin

__models = {}


def odm_register_model(model: str, cls: type):
    """Register UI model.
    """

    # Just for debugging purposes
    if model in __models:
        raise KeyError("Model '{}' is already registered.".format(model))

    # Checking inheritance
    mock = odm.manager.dispense(model)
    if not isinstance(mock, ODMUIMixin):
        return

    assert isinstance(mock, odm.model.ODMModel)  # Just for correct type hinting in PyCharm
    pkg_name = mock.package()

    # Registering package's language container
    if not lang.is_package_registered(pkg_name):
        lang.register_package(pkg_name)

    # Registering permission group if doesn't already registered
    permission_group = pkg_name
    if not _manager.get_permission_group(permission_group):
        _manager.define_permission_group(permission_group, pkg_name + '@odm_ui_permission_group_description')

    # Registering permissions
    for perm_name in 'create', 'browse', 'browse_own', 'modify', 'modify_own', 'delete', 'delete_own':
        if perm_name.endswith('_own') and not mock.has_field('author'):
            continue
        perm_description = pkg_name + '@odm_ui_permission_' + perm_name + '_' + model
        perm_full_name = 'pytsite.odm_ui.' + perm_name + '.' + model
        _manager.define_permission(perm_full_name, perm_description, pkg_name)

    __models[model] = model