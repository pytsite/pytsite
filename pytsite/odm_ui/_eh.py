"""ODM UI Manager.
"""
from pytsite import lang as _lang, odm as _odm, auth as _auth, permission as _permission
from ._entity import UIMixin

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_models = {}


def odm_register_model(model: str, cls, replace: bool):
    """'pytsite.odm.register_model' event handler.
    """
    if model in _models and not replace:
        raise KeyError("Model '{}' is already registered os odm_ui model.".format(model))

    # Checking inheritance
    if not issubclass(cls, UIMixin):
        return

    # Determining model's package name
    pkg_name = cls.package_name()

    # Registering package's language resources
    if not _lang.is_package_registered(pkg_name):
        _lang.register_package(pkg_name)

    # Registering permission group if it doesn't already registered
    if not _permission.is_permission_group_defined(pkg_name):
        _permission.define_permission_group(pkg_name, pkg_name + '@odm_ui_permission_group_description')

    # Registering permissions
    mock = _odm.dispense(model)
    if model not in _models:
        for perm_name in 'create', 'browse', 'browse_own', 'modify', 'modify_own', 'delete', 'delete_own':
            if perm_name.endswith('_own') and not mock.has_field('author') and not mock.has_field('owner'):
                continue

            perm_full_name = 'pytsite.odm_ui.' + perm_name + '.' + model
            perm_description = cls.resolve_partly_msg_id('odm_ui_permission_' + perm_name + '_' + model)
            _permission.define_permission(perm_full_name, perm_description, pkg_name)

    _models[model] = model
