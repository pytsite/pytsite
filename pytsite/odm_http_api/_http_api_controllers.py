""" PytSite ODM HTTP API
"""
from typing import Mapping as _Mapping, List as _List
from json import loads as _json_loads, JSONDecodeError as _JSONDecodeError
from pytsite import odm as _odm, odm_auth as _odm_auth, routing as _routing, formatters as _formatters

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _fill_entity_fields(entity: _odm_auth.model.AuthorizableEntity,
                        fields_data: _Mapping) -> _odm_auth.model.AuthorizableEntity:
    for k, v in fields_data.items():
        # Fields to skip
        if k.startswith('_'):
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


def _parse_query(query: str, finder: _odm.Finder) -> _odm.Finder:
    if not query:
        return finder

    for query_part in query.split(';'):
        try:
            f_name, op, arg = query_part.split('~')
            finder.where(f_name, op, arg)
        except ValueError:
            raise ValueError('Invalid query: {}'.format(query))

    return finder


class GetEntities(_routing.Controller):
    """Get entities
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('skip', _formatters.PositiveInt())
        self.args.add_formatter('limit', _formatters.Int(0, 100))

    def exec(self) -> _List[dict]:
        model = self.args.pop('model')

        # Check entity's class
        try:
            mock = _odm.dispense(model)
            if not isinstance(mock, _odm_auth.model.AuthorizableEntity):
                raise self.forbidden("Model '{}' does not support transfer via HTTP".format(model))
        except _odm.error.ModelNotRegistered as e:
            raise self.not_found(e)

        # Which fields to return
        fields = self.args.pop('fields_list')
        if isinstance(fields, str):
            fields = fields.split(',')

        r = []
        f = _parse_query(self.args.pop('query'), _odm.find(model)).skip(self.args.pop('skip', 0))
        for entity in f.get(self.args.pop('limit', 100)):
            if not entity.odm_auth_check_permission('view'):
                continue

            jsonable = entity.as_jsonable(**dict(self.args))

            r.append({k: v for k, v in jsonable.items() if k in fields} if fields else jsonable)

        return r


class GetEntity(_routing.Controller):
    """Get an entity
    """

    def exec(self) -> dict:
        model = self.arg('model')

        # Search for entity
        try:
            entity = _odm.find(model).eq('_id', self.arg('uid')).first()  # type: _odm_auth.model.AuthorizableEntity
        except _odm.error.ModelNotRegistered as e:
            raise self.not_found(e)

        if not entity:
            raise self.not_found('Entity not found')

        # Check for entity's class
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.forbidden("Model '{}' does not support transfer via HTTP".format(model))

        # Check for permissions
        if not entity.odm_auth_check_permission('view'):
            raise self.forbidden('Insufficient permissions')

        # Which fields to return
        fields = self.args.pop('fields_list')
        if isinstance(fields, str):
            fields = fields.split(',')

        jsonable = entity.as_jsonable(**dict(self.args))

        return {k: v for k, v in jsonable.items() if k in fields} if fields else jsonable


class PostEntity(_routing.Controller):
    """Create a new entity
    """

    def exec(self) -> dict:
        model = self.args.pop('model')

        # Check permissions
        if not _odm_auth.check_permission('create', model):
            raise self.forbidden('Insufficient permissions')

        # Dispense new entity
        try:
            entity = _odm.dispense(model)  # type: _odm_auth.model.AuthorizableEntity
        except _odm.error.ModelNotRegistered as e:
            raise self.not_found(e)

        # Only authorizable entities can be accessed via HTTP API
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.forbidden("Model '{}' does not support transfer via HTTP".format(model))

        # Which fields to return
        fields = self.args.pop('fields_list')
        if isinstance(fields, str):
            fields = fields.split(',')

        # Fill entity's fields with values and save
        _fill_entity_fields(entity, self.args).save()

        jsonable = entity.as_jsonable()

        return {k: v for k, v in jsonable.items() if k in fields} if fields else jsonable


class PatchEntity(_routing.Controller):
    """Update an entity
    """

    def exec(self) -> dict:
        model = self.args.pop('model')

        # Dispense existing entity
        try:
            entity = _odm.dispense(model, self.args.pop('uid'))  # type: _odm_auth.model.AuthorizableEntity
        except _odm.error.ModelNotRegistered as e:
            raise self.not_found(e)

        # Only authorizable entities can be accessed via HTTP API
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.forbidden("Model '{}' does not support transfer via HTTP".format(model))

        # Check permissions
        if not (entity.odm_auth_check_permission('modify') or entity.odm_auth_check_permission('modify_own')):
            raise self.forbidden('Insufficient permissions')

        # Which fields to return
        fields = self.args.pop('fields_list')
        if isinstance(fields, str):
            fields = fields.split(',')

        # Fill fields with values and save
        _fill_entity_fields(entity, self.args).save()

        jsonable = entity.as_jsonable()

        return {k: v for k, v in jsonable.items() if k in fields} if fields else jsonable


class DeleteEntity(_routing.Controller):
    """Delete an entity
    """

    def exec(self) -> dict:
        model = self.arg('model')

        try:
            # Dispense existing entity
            entity = _odm.dispense(model, self.arg('uid'))
        except _odm.error.ModelNotRegistered as e:
            raise self.not_found(e)

        # Only authorizable entities can be accessed via HTTP API
        if not isinstance(entity, _odm_auth.model.AuthorizableEntity):
            raise self.forbidden("Model '{}' does not support transfer via HTTP".format(model))

        # Check permissions
        if not (entity.odm_auth_check_permission('delete') or entity.odm_auth_check_permission('delete_own')):
            raise self.forbidden('Insufficient permissions')

        # Delete entity
        try:
            entity.delete()
        except _odm.error.EntityDeleted:
            # Entity was deleted by another instance
            pass

        return {'status': True}
