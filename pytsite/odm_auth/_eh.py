"""PytSite ODM UI Event Handlers.
"""
from pytsite import lang as _lang, odm as _odm, permissions as _permission, logger as _logger, auth as _auth, \
    errors as _errors
from . import _model

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
    pkg_name = cls.get_package_name()

    # Registering package's language resources
    if not _lang.is_package_registered(pkg_name):
        _lang.register_package(pkg_name)

    # Register permissions
    perm_group = cls.odm_auth_permissions_group()
    if perm_group:
        # Registering permissions
        mock = _odm.dispense(model)  # type: _model.AuthorizableEntity
        for perm_name in mock.odm_auth_permissions():
            if perm_name.endswith('_own') and not mock.has_field('author') and not mock.has_field('owner'):
                continue

            p_name = 'pytsite.odm_perm.' + perm_name + '.' + model
            if not _permission.is_permission_defined(p_name):
                p_description = cls.resolve_partly_msg_id('odm_perm_' + perm_name + '_' + model)
                _permission.define_permission(p_name, p_description, perm_group)


def odm_entity_pre_save(entity: _model.AuthorizableEntity):
    """'pytsite.odm.entity_pre_save' event handler.
    """
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
        raise _errors.ForbidCreation("Insufficient permissions to create entities of model '{}'.".
                                     format(entity.model))

    # Check current user's permissions to MODIFY entities
    elif not entity.is_new and not entity.check_permissions('modify'):
        _logger.info('Current user login: {}'.format(_auth.get_current_user().login))
        raise _errors.ForbidModification("Insufficient permissions to modify entity '{}:{}'.".
                                         format(entity.model, entity.id))


def odm_entity_pre_delete(entity: _model.AuthorizableEntity):
    """'pytsite.odm.entity_pre_delete' event handler.
    """
    # Check if the model supports permissions
    if not isinstance(entity, _model.AuthorizableEntity):
        return

    c_user = _auth.get_current_user()

    # System user and admins have unrestricted permissions
    if c_user.is_system or c_user.is_admin:
        return

    # Check current user's permissions to DELETE entities
    if not entity.check_permissions('delete'):
        _logger.debug('Current user login: {}'.format(_auth.get_current_user().login))
        raise _errors.ForbidDeletion("Insufficient permissions to delete entity '{}:{}'.".
                                     format(entity.model, entity.id))
