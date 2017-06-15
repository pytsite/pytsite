""" PytSite ODM Auth HTTP API.
"""
from json import loads as _json_loads, JSONDecodeError as _JSONDecodeError
from pytsite import odm as _odm, odm_auth as _odm_auth, routing as _routing

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _fill_entity_fields(entity: _odm_auth.model.AuthorizableEntity, inp: dict) -> _odm_auth.model.AuthorizableEntity:
    for k, v in inp.items():
        # Fields to skip
        if k == 'access_token' or k.startswith('_'):
            continue

        field = entity.get_field(k)

        # Convert JSON string to object
        if isinstance(field, (_odm.field.List, _odm.field.Dict)):
            if isinstance(v, str):
                try:
                    v = _json_loads(v)
                except _JSONDecodeError as e:
                    raise RuntimeError("JSON decoding error at field '{}': {}".format(k, e))
            else:
                raise RuntimeError("Field '{}' is not properly JSON-encoded".format(k))

        # Resolve references
        if isinstance(field, _odm.field.Ref):
            v = _odm.resolve_ref(v, field.model)
        elif isinstance(field, _odm.field.RefsList):
            v = _odm.resolve_refs(v, field.model)

        # Set field's value
        try:
            entity.f_set(k, v)
        except (TypeError, ValueError) as e:
            raise RuntimeError("Invalid format of field '{}': {}".format(k, e))

    return entity


class PostEntity(_routing.Controller):
    """Create new entity
    """

    def exec(self) -> dict:
        # Check permissions
        if not _odm_auth.check_permission('create', self.arg('model')):
            raise self.forbidden('Insufficient permissions')

        # Dispense new entity
        entity = _odm.dispense(self.arg('model'))  # type: _odm_auth.model.AuthorizableEntity

        # Only authorizable entities can be accessed via HTTP API
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.forbidden("Model '{}' does not support transfer via HTTP.")

        # Fill entity's fields with values and save
        _fill_entity_fields(entity, self.args).save()

        return entity.as_jsonable()


class GetEntity(_routing.Controller):
    """Get entity
    """

    def exec(self) -> dict:
        # Search for entity
        entity = _odm.find(self.arg('model')) \
            .eq('_id', self.arg('uid')).first()  # type: _odm_auth.model.AuthorizableEntity

        if not entity:
            raise self.not_found('Entity not found')

        # Check for entity's class
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.server_error("Model '{}' does not support transfer via HTTP.")

        # Check for permissions
        if not entity.odm_auth_check_permission('view'):
            raise self.forbidden('Insufficient permissions')

        return entity.as_jsonable(**self.args)


class PatchEntity(_routing.Controller):
    """Update entity
    """

    def exec(self) -> dict:
        # Dispense existing entity
        entity = _odm.dispense(self.arg('model'), self.arg('uid'))  # type: _odm_auth.model.AuthorizableEntity

        # Only authorizable entities can be accessed via HTTP API
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.server_error("Model '{}' does not support transfer via HTTP.")

        # Check permissions
        if not (entity.odm_auth_check_permission('modify') or entity.odm_auth_check_permission('modify_own')):
            raise self.forbidden('Insufficient permissions')

        # Fill fields with values and save
        with entity:
            _fill_entity_fields(entity, self.args).save()

        return entity.as_jsonable()


class DeleteEntity(_routing.Controller):
    """Delete an entity
    """

    def exec(self) -> dict:
        # Dispense existing entity
        entity = _odm.dispense(self.arg('model'), self.arg('uid'))

        # Only authorizable entities can be accessed via HTTP API
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.server_error("Model '{}' does not support transfer via HTTP.")

        # Check permissions
        if not (entity.odm_auth_check_permission('delete') or entity.odm_auth_check_permission('delete_own')):
            raise self.forbidden('Insufficient permissions')

        # Delete entity
        with entity:
            entity.delete()

        return {'status': True}
