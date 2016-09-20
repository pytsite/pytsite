""" PytSite ODM Auth HTTP API
"""
from json import loads as _json_loads, JSONDecodeError as _JSONDecodeError
from pytsite import http as _http, odm as _odm
from . import _model, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _fill_entity_fields(entity: _model.AuthorizableEntity, inp: dict):
    for k, v in inp.items():
        # Fields to skip
        if k in ('access_token', 'model', 'uid') or k.startswith('_'):
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
        except (TypeError, ValueError):
            raise _http.error.InternalServerError("Invalid format of field '{}'".format(k))


def get_entity(inp: dict) -> dict:
    """Get entity.
    """
    model = inp.get('model')
    if not model:
        raise _http.error.InternalServerError('Model is not specified.')

    uid = inp.get('uid')
    if not uid:
        raise _http.error.InternalServerError('UID is not specified.')

    # Search for entity
    entity = _odm.find(model).eq('_id', uid).first()  # type: _model.AuthorizableEntity
    if not entity:
        raise _http.error.NotFound('Entity not found.')

    # Check for entity's class
    if not isinstance(entity, _model.AuthorizableEntity):
        raise _http.error.InternalServerError("Model '{}' does not support transfer via HTTP.")

    # Check for permissions
    if not entity.check_permissions('view'):
        raise _http.error.Forbidden('Insufficient permissions.')

    return entity.as_jsonable(**inp)


def post_entity(inp: dict):
    """Create new entity.
    """
    # Required arguments
    model = inp.get('model')
    if not model:
        raise _http.error.InternalServerError('Model is not specified.')

    # Check permissions
    if not _api.check_permissions('create', model):
        raise _http.error.Forbidden("Insufficient permissions.")

    # Dispense new entity
    entity = _api.dispense(model)

    # Fill fields with values
    _fill_entity_fields(entity, inp)
    entity.save()

    return entity.as_jsonable()


def patch_entity(inp: dict) -> dict:
    """Update entity.
    """
    # Model is required
    model = inp.get('model')
    if not model:
        raise RuntimeError('Model is not specified.')

    # Entity ID is required
    uid = inp.get('uid')
    if not uid:
        raise RuntimeError('UID is not specified.')

    # Dispense existing entity
    entity = _api.dispense(model, uid)

    # Check permissions
    if not entity.check_permissions('modify'):
        raise _http.error.Forbidden("Insufficient permissions.")

    # Fill fields with values
    with entity:
        _fill_entity_fields(entity, inp)
        entity.save()

    return entity.as_jsonable()


def delete_entity(inp: dict):
    """Delete one or more entities.
    """
    model = inp.get('model')
    ids = inp.get('uid')

    if not model:
        raise RuntimeError('Model is not specified.')

    if not ids:
        raise RuntimeError('IDs are not specified.')

    if isinstance(ids, str):
        ids = (ids,)

    count = 0
    for eid in ids:
        entity = _odm.dispense(model, eid)
        with entity:
            entity.delete()
        count += 1

    return count
