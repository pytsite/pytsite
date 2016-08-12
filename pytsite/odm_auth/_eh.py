"""ODM UI Manager.
"""
from pytsite import lang as _lang, odm as _odm, permission as _permission, logger as _logger, auth as _auth
from . import _model, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def odm_register_model(model: str, cls, replace: bool):
    """'pytsite.odm.register_model' event handler.
    """
    # Check if the model supports permissions
    if not issubclass(cls, _model.AuthorizableEntity):
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
    mock = _odm.dispense(model)  # type: _model.AuthorizableEntity
    for perm_name in mock.get_permissions():
        if perm_name.endswith('_own') and not mock.has_field('author') and not mock.has_field('owner'):
            continue

        p_name = 'pytsite.odm_perm.' + perm_name + '.' + model
        if not _permission.is_permission_defined(p_name):
            p_description = cls.resolve_partly_msg_id('odm_perm_' + perm_name + '_' + model)
            _permission.define_permission(p_name, p_description, pkg_name)


def odm_entity_pre_save(entity: _model.AuthorizableEntity):
    """'pytsite.odm.entity_pre_save' event handler.
    """
    # Is permissions checking enabled
    if not _api.is_perm_check_enabled():
        return

    # Check if the model supports permissions
    if not isinstance(entity, _model.AuthorizableEntity):
        return

    c_user = _auth.get_current_user()

    # System user and admins have unrestricted permissions
    if c_user.is_system or c_user.is_admin:
        return

    # Check current user's permissions to MODIFY entities
    if entity.is_new and not entity.check_permissions('create'):
        _logger.info('Current user login: {}'.format(_auth.get_current_user().login))
        raise _odm.error.ForbidEntityCreate("Insufficient permissions to create entities of model '{}'.".
                                            format(entity.model))

    # Check current user's permissions to MODIFY entities
    elif not entity.is_new and not entity.check_permissions('modify'):
        _logger.info('Current user login: {}'.format(_auth.get_current_user().login))
        raise _odm.error.ForbidEntityModify("Insufficient permissions to modify entity '{}:{}'.".
                                            format(entity.model, entity.id))


def odm_entity_pre_delete(entity: _model.AuthorizableEntity):
    """'pytsite.odm.entity_pre_delete' event handler.
    """
    # Is permissions checking enabled
    if not _api.is_perm_check_enabled():
        return

    # Check if the model supports permissions
    if not isinstance(entity, _model.AuthorizableEntity):
        return

    c_user = _auth.get_current_user()

    # System user and admins have unrestricted permissions
    if c_user.is_system or c_user.is_admin:
        return

    # Check current user's permissions to DELETE entities
    if not entity.check_permissions('delete'):
        _logger.info('Current user login: {}'.format(_auth.get_current_user().login))
        raise _odm.error.ForbidEntityDelete("Insufficient permissions to delete entity '{}:{}'.".
                                            format(entity.model, entity.id))
