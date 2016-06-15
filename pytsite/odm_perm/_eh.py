"""ODM UI Manager.
"""
from typing import Union as _Union
from pytsite import lang as _lang, odm as _odm, permission as _permission
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def odm_register_model(model: str, cls, replace: bool):
    """'pytsite.odm.register_model' event handler.
    """

    # Checking inheritance
    if not issubclass(cls, _model.PermMixin):
        return

    # Determining model's package name
    pkg_name = cls.package_name()

    # Registering package's language resources
    if not _lang.is_package_registered(pkg_name):
        _lang.register_package(pkg_name)

    # Registering permission group if it doesn't already registered
    if not _permission.is_permission_group_defined(pkg_name):
        _permission.define_permission_group(pkg_name, pkg_name + '@odm_perm_group_description')

    # Registering permissions
    mock = _odm.dispense(model)
    for perm_name in ('create', 'view', 'modify', 'delete'):
        # Define 'global' permission
        p_name = 'pytsite.odm_perm.' + perm_name + '.' + model
        p_description = cls.resolve_partly_msg_id('odm_perm_' + perm_name + '_' + model)
        _permission.define_permission(p_name, p_description, pkg_name)

        if perm_name != 'create' and (mock.has_field('author') or mock.has_field('owner')):
            p_name = 'pytsite.odm_perm.' + perm_name + '_own.' + model
            p_description = cls.resolve_partly_msg_id('odm_perm_' + perm_name + '_own_' + model)
            _permission.define_permission(p_name, p_description, pkg_name)


def odm_entity_pre_save(entity: _Union[_odm.model.Entity, _model.PermMixin]):
    """'pytsite.odm.entity_pre_save' event handler.
    """
    if not isinstance(entity, _model.PermMixin):
        return

    if entity.is_new and not entity.perm_check('create'):
        raise _odm.error.ForbidEntityCreate("Insufficient permissions to create entities of model '{}'.".
                                            format(entity.model))

    elif not entity.is_new and not entity.perm_check('modify'):
        raise _odm.error.ForbidEntityModify("Insufficient permissions to modify entity '{}:{}'.".
                                            format(entity.model, entity.id))


def odm_entity_pre_delete(entity: _Union[_odm.model.Entity, _model.PermMixin]):
    """'pytsite.odm.entity_pre_delete' event handler.
    """
    if not isinstance(entity, _model.PermMixin):
        return

    if not entity.perm_check('delete'):
        raise _odm.error.ForbidEntityDelete("Insufficient permissions to delete entity '{}:{}'.".
                                            format(entity.model, entity.id))
