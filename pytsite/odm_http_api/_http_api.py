""" PytSite ODM Auth HTTP API.
"""
from json import loads as _json_loads, JSONDecodeError as _JSONDecodeError
from pytsite import http as _http, odm as _odm, odm_auth as _odm_auth

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
                    raise _http.error.InternalServerError("JSON decoding error at field '{}': {}".format(k, e))
            else:
                raise _http.error.InternalServerError("Field '{}' is not properly JSON-encoded".format(k))

        # Resolve references
        if isinstance(field, _odm.field.Ref):
            v = _odm.resolve_ref(v, field.model)
        elif isinstance(field, _odm.field.RefsList):
            v = _odm.resolve_refs(v, field.model)

        # Set field's value
        try:
            entity.f_set(k, v)
        except (TypeError, ValueError) as e:
            raise _http.error.InternalServerError("Invalid format of field '{}': {}".format(k, e))

    return entity


def post_entity(inp: dict, model: str) -> dict:
    """Create new entity.
    """
    # Check for permissions
    if not _odm_auth.check_permission('create', model):
        raise _http.error.Forbidden('Insufficient permissions')

    # Dispense new entity
    entity = _odm.dispense(model)  # type: _odm_auth.model.AuthorizableEntity

    # Only authorizable entities can be accessed via HTTP API
    if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
        raise _http.error.Forbidden("Model '{}' does not support transfer via HTTP.")

    # Fill entity's fields with values and save
    _fill_entity_fields(entity, inp).save()

    return entity.as_jsonable()


def get_entity(inp: dict, model: str, uid: str) -> dict:
    """Get entity.
    """
    # Search for entity
    entity = _odm.find(model).eq('_id', uid).first()  # type: _odm_auth.model.AuthorizableEntity
    if not entity:
        raise _http.error.NotFound('Entity not found.')

    # Check for entity's class
    if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
        raise _http.error.InternalServerError("Model '{}' does not support transfer via HTTP.")

    # Check for permissions
    if not entity.odm_auth_check_permission('view'):
        raise _http.error.Forbidden('Insufficient permissions')

    return entity.as_jsonable(**inp)


def patch_entity(inp: dict, model: str, uid: str) -> dict:
    """Update entity.
    """
    # Dispense existing entity
    entity = _odm.dispense(model, uid)

    # Only authorizable entities can be accessed via HTTP API
    if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
        raise _http.error.InternalServerError("Model '{}' does not support transfer via HTTP.")

    # Check permissions
    if not (entity.odm_auth_check_permission('modify') or entity.odm_auth_check_permission('modify_own')):
        raise _http.error.Forbidden('Insufficient permissions')

    # Fill fields with values and save
    with entity:
        _fill_entity_fields(entity, inp).save()

    return entity.as_jsonable()


def delete_entity(inp: dict, model: str, uid: str) -> dict:
    """Delete one or more entities.
    """
    # Dispense existing entity
    entity = _odm.dispense(model, uid)

    # Only authorizable entities can be accessed via HTTP API
    if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
        raise _http.error.InternalServerError("Model '{}' does not support transfer via HTTP.")

    # Check permissions
    if not (entity.odm_auth_check_permission('delete') or entity.odm_auth_check_permission('delete_own')):
        raise _http.error.Forbidden('Insufficient permissions')

    # Delete entity
    with entity:
        entity.delete()

    return {'status': True}
