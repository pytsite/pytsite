"""ODM UI Manager.
"""
from pytsite import lang as _lang, odm as _odm, auth as _auth
from ._model import UIMixin

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__models = {}


def odm_register_model(model: str, cls, replace: bool):
    """Register UI model.
    """
    if model in __models and not replace:
        raise KeyError("Model '{}' is already registered os odm_ui model.".format(model))

    # Checking inheritance
    if not issubclass(cls, UIMixin):
        return

    # Detecting model's package name
    pkg_name = cls.package_name()

    # Registering package's language container
    if not _lang.is_package_registered(pkg_name):
        _lang.register_package(pkg_name)

    # Registering permission group if doesn't already registered
    if not _auth.get_permission_group(pkg_name):
        _auth.define_permission_group(pkg_name, pkg_name + '@odm_ui_permission_group_description')

    # Registering permissions
    mock = _odm.dispense(model)
    if model not in __models:
        for perm_name in 'create', 'browse', 'browse_own', 'modify', 'modify_own', 'delete', 'delete_own':
            if perm_name.endswith('_own') and not mock.has_field('author') and not mock.has_field('owner'):
                continue

            perm_full_name = 'pytsite.odm_ui.' + perm_name + '.' + model
            perm_description = cls.resolve_partly_msg_id('odm_ui_permission_' + perm_name + '_' + model)
            _auth.define_permission(perm_full_name, perm_description, pkg_name)

    __models[model] = model
