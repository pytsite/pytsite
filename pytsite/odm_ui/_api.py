"""ODM UI Manager.
"""
from typing import Iterable as _Iterable
from pytsite import auth as _auth, router as _router, metatag as _metatag, odm as _odm, lang as _lang, http as _http, \
    form as _form, widget as _widget, html as _html
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_m_form(model: str, eid=None, stage: str='show', form_uid='odm-ui-form') -> _form.Form:
    """Get entity modification _form.
    """
    eid = eid if eid != '0' else None

    # Checking permissions
    if not eid and not check_permissions('create', model):
        raise _http.error.Forbidden()
    if eid and not check_permissions('modify', model, eid):
        raise _http.error.Forbidden()

    # Checking model settings
    model_class = _odm.get_model_class(model)
    """:type: _model.UIModel"""
    if not eid and not model_class.ui_is_creation_allowed():
        raise _http.error.Forbidden()
    if eid and not model_class.ui_is_modification_allowed():
        raise _http.error.Forbidden()

    # Creating form
    frm = _form.Form(form_uid)
    frm.css += ' odm-ui-form odm-ui-form-' + model

    # Action, redirect and validation endpoints
    frm.validation_ep = 'pytsite.odm_ui.ep.validate_m_form'
    frm.action = _router.ep_url('pytsite.odm_ui.ep.post_m_form', {'model': model, 'id': eid if eid else '0'})
    if not _router.request.inp.get('__form_redirect'):
        frm.redirect = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model})

    # Action buttons
    submit_button = _widget.button.Submit(weight=10, uid='action_submit', value=_lang.t('pytsite.odm_ui@save'),
                                          color='primary', icon='fa fa-save')
    cancel_button = _widget.button.Link(weight=20, uid='action_cancel', value=_lang.t('pytsite.odm_ui@cancel'),
                                        href=frm.redirect, icon='fa fa-remove')
    actions = _widget.static.Container(
        uid='actions',
        css='actions-wrapper text-xs-B-center text-sm-left',
        form_area='footer',
    )
    actions.append(submit_button).append(cancel_button)
    frm.add_widget(actions)

    # Metadata
    frm.add_widget(_widget.input.Hidden(uid='__odm_ui_model', value=model, form_area='hidden'))
    frm.add_widget(_widget.input.Hidden(uid='__odm_ui_entity_id', value=eid, form_area='hidden'))

    entity = dispense_entity(model, eid)

    # Legend
    if entity.is_new:
        legend = entity.t('odm_ui_form_title_create_' + model)
    else:
        legend = entity.t('odm_ui_form_title_modify_' + model)

    _metatag.t_set('title', legend)

    # Setting up the form with entity hook
    entity.ui_m_form_setup(frm, stage)

    return frm


def get_mass_action_form(fid: str, model: str, ids: _Iterable, action: str, redirect: str=None) -> _form.Form:
    f = _form.Form(fid, action=action)

    # List of items to process
    ol = _html.Ol()
    for eid in ids:
        entity = dispense_entity(model, eid)
        f.add_widget(_widget.input.Hidden(uid='ids-' + eid, name='ids', value=eid))
        ol.append(_html.Li(entity.ui_mass_action_get_entity_description()))
    f.add_widget(_widget.static.HTMLWrap(uid='ids-text', em=ol))

    # Redirect
    if redirect:
        f.redirect = redirect
    else:
        f.redirect = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model})

    # Continue button
    submit_button = _widget.button.Submit(uid='button-submit', weight=10, value=_lang.t('pytsite.odm_ui@continue'),
                                          color='primary', icon='angle-double-right', form_area='footer')

    # Cancel button
    cancel_button = _widget.button.Link(uid='button-cancel', weight=20, value=_lang.t('pytsite.odm_ui@cancel'),
                                        href=f.redirect, icon='ban', form_area='footer')
    f.add_widget(submit_button).add_widget(cancel_button)

    return f


def get_d_form(model: str, ids: _Iterable, redirect: str=None) -> _form.Form:
    """Get entities delete _form.
    """
    model_class = _odm.get_model_class(model)
    """:type: _model.UIModel"""

    if not check_permissions('delete', model, ids) or not model_class.ui_is_deletion_allowed():
        raise _http.error.Forbidden()

    # Setup form
    f_action = _router.ep_url('pytsite.odm_ui.ep.post_d_form', {'model': model})
    f = get_mass_action_form('odm-ui-delete-form', model, ids, f_action, redirect)

    # Change submit button color
    submit_btn = f.get_widget('button-submit')
    submit_btn.color = 'danger'

    _metatag.t_set('title', model_class.t('odm_ui_form_title_delete_' + model))

    return f


def dispense_entity(model: str, entity_id: str=None):
    """Dispense entity.

    :rtype: _model.UIModel
    """
    if not entity_id or entity_id == '0':
        entity_id = None
    entity = _odm.dispense(model, entity_id)
    if not isinstance(entity, _model.UIMixin):
        raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(model))

    return entity


def check_permissions(perm_type: str, model: str, ids=None) -> bool:
    """Check current user's permissions to operate with entity(es).

    :param perm_type: Valid types: 'create', 'browse', 'modify', 'delete'
    """
    current_user = _auth.get_current_user()

    # Anonymous user cannot do anything
    if current_user.is_anonymous:
        return False

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
    elif perm_type in ('browse', 'modify', 'delete'):
        # User can browse, modify or delete ANY entity of this model
        if current_user.has_permission('pytsite.odm_ui.' + perm_type + '.' + model):
            return True

        # User can browse, modify or delete ONLY ITS OWN entity of this model
        elif ids:
            own_perm_name = 'pytsite.odm_ui.' + perm_type + '_own.' + model
            if _auth.get_permission(own_perm_name) and current_user.has_permission(own_perm_name):
                for eid in ids:
                    entity = dispense_entity(model, eid)
                    if not entity:
                        return False
                    if entity.has_field('author') and not entity.f_get('author').id == current_user.id:
                        return False
                    if entity.has_field('owner') and not entity.f_get('owner').id == current_user.id:
                        return False
                return True

    return False
