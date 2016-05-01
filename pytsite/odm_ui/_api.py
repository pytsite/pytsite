"""ODM UI Manager.
"""
from typing import Iterable as _Iterable
from pytsite import auth as _auth, odm as _odm, form as _form
from . import _entity, _forms

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_m_form(model: str, eid=None, update_meta_title: bool = True, **kwargs) -> _forms.Modify:
    """Get entity modification form.
    """
    return _forms.Modify('odm-ui-form-' + model, model=model, eid=eid if eid != '0' else None,
                         update_meta_title=update_meta_title, **kwargs)


def get_d_form(model: str, ids: _Iterable, redirect: str = None) -> _form.Form:
    """Get entities delete form.
    """
    return _forms.Delete('odm-ui-d-form', model=model, eids=ids, redirect=redirect)


def get_model_class(model: str) -> _entity.UIEntity:
    """Get ODM UI model class.
    """
    model_class = _odm.get_model_class(model)
    if not issubclass(model_class, _entity.UIMixin):
        raise TypeError("Model '{}' must extend 'UIMixin'".format(model))

    return model_class


def dispense_entity(model: str, entity_id: str = None) -> _entity.UIEntity:
    """Dispense entity.
    """
    if not entity_id or entity_id == '0':
        entity_id = None

    entity = _odm.dispense(model, entity_id)

    if not isinstance(entity, _entity.UIMixin):
        raise TypeError("Model '{}' must extend 'UIMixin'".format(model))

    return entity


def check_permissions(perm_type: str, model: str, ids: _Iterable = None) -> bool:
    """Check current user's permissions to operate with entity(es).

    :param perm_type: Valid types are: 'create', 'browse', 'modify', 'delete'
    """
    # Get current user
    current_user = _auth.get_current_user()

    # Anonymous user cannot do anything
    if current_user.is_anonymous:
        return False

    # Check ids type
    if ids and type(ids) not in (list, tuple):
        ids = (ids,)

    # Ability for users to modify themselves
    if perm_type == 'modify' and model == 'user' and len(ids) == 1:
        user = _auth.get_user(uid=ids[0])
        if user and user.id == current_user.id:
            return True

    if perm_type == 'create':
        if current_user.has_permission('pytsite.odm_ui.create.' + model):
            return True
    else:
        # If user has global permissions for model
        if current_user.has_permission('pytsite.odm_ui.' + perm_type + '.' + model):
            return True

        # User can browse, modify or delete ONLY ITS OWN entity of this model
        elif ids and current_user.has_permission('pytsite.odm_ui.' + perm_type + '_own.' + model):
            # Check each entity
            for eid in ids:
                entity = dispense_entity(model, eid)

                # Anyone cannot do anything with non-existent entities
                if not entity:
                    return False

                # Searching for author of the entity
                for author_field in 'author', 'owner':
                    if entity.has_field(author_field) and entity.f_get(author_field).id == current_user.id:
                        return True

    return False
