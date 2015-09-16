"""ODM UI Manager.
"""
from pytsite import lang as _lang, odm as _odm, auth as _auth
from ._model import UIMixin

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__models = {}


def odm_register_model(model: str, cls: type, replace: bool):
    """Register UI model.
    """
    if model in __models and not replace:
        raise KeyError("Model '{}' is already registered.".format(model))

    # Checking inheritance
    mock = _odm.dispense(model)
    if not isinstance(mock, UIMixin):
        return

    assert isinstance(mock, _odm.Model)  # Just for correct type hinting in PyCharm
    pkg_name = mock.package_name()

    # Registering package's language container
    if not _lang.is_package_registered(pkg_name):
        _lang.register_package(pkg_name)

    # Registering permission group if doesn't already registered
    permission_group = pkg_name
    if not _auth.get_permission_group(permission_group):
        _auth.define_permission_group(permission_group, pkg_name + '@odm_ui_permission_group_description')

    # Registering permissions
    if model not in __models:
        for perm_name in 'create', 'browse', 'browse_own', 'modify', 'modify_own', 'delete', 'delete_own':
            if perm_name.endswith('_own') and not mock.has_field('author') and not mock.has_field('owner'):
                continue
            perm_description = pkg_name + '@odm_ui_permission_' + perm_name + '_' + model
            perm_full_name = 'pytsite.odm_ui.' + perm_name + '.' + model
            _auth.define_permission(perm_full_name, perm_description, pkg_name)

    __models[model] = model
