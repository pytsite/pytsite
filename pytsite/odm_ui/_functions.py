"""ODM UI Manager.
"""
from pytsite import auth as _auth, router as _router, metatag as _metatag, odm as _odm, lang as _lang, http as _http, \
    form as _form, widget as _widget, html as _html
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_m_form(model: str, eid: str=None, stage: str='show') -> _form.Base:
    """Get entity modification _form.
    """
    eid = eid if eid != '0' else None

    # Checking permissions
    if not eid and not check_permissions('create', model):
        raise _http.error.Forbidden()
    elif eid and not check_permissions('modify', model, [eid]):
        raise _http.error.Forbidden()

    # Creating form
    frm = _form.Base('odm-ui-form')
    frm.css += ' odm-ui-form odm-ui-form-' + model

    # Action, redirect and validation endpoints
    frm.validation_ep = 'pytsite.odm_ui.ep.validate_m_form'
    frm.action = _router.ep_url('pytsite.odm_ui.ep.post_m_form', {'model': model, 'id': eid if eid else '0'})
    if not _router.request.values_dict.get('__form_redirect'):
        frm.redirect = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model})

    # Action buttons
    submit_button = _widget.button.Submit(weight=10, uid='action_submit', value=_lang.t('pytsite.odm_ui@save'),
                                          color='primary', icon='fa fa-save')
    cancel_button = _widget.button.Link(weight=20, uid='action_cancel', value=_lang.t('pytsite.odm_ui@cancel'),
                                        href=frm.redirect, icon='fa fa-remove')
    actions_wrapper = _widget.static.Wrapper(uid='actions', css='actions-wrapper text-xs-B-center text-sm-left')
    actions_wrapper.add_child(submit_button).add_child(cancel_button)
    frm.add_widget(actions_wrapper, area='footer')

    # Metadata
    frm.add_widget(_widget.input.Hidden(uid='__model', value=model), area='form')
    frm.add_widget(_widget.input.Hidden(uid='__entity_id', value=eid), area='form')

    entity = dispense_entity(model, eid)

    # Legend
    if entity.is_new:
        legend = entity.t('odm_ui_form_legend_create_' + model)
    else:
        legend = entity.t('odm_ui_form_legend_modify_' + model)

    _metatag.t_set('title', legend)

    # Setting up the form with entity hook
    entity.setup_m_form(frm, stage)

    return frm


def get_d_form(model: str, ids: list, redirect: str=None) -> _form.Base:
    """Get entities delete _form.
    """
    if not check_permissions('delete', model, ids):
        raise _http.error.Forbidden()

    # Form
    frm = _form.Base('odm-ui-delete-form')
    frm.action = _router.ep_url('pytsite.odm_ui.ep.post_d_form', {'model': model})
    if redirect:
        frm.redirect = redirect

    mock = dispense_entity(model)
    _metatag.t_set('title', mock.t('odm_ui_form_legend_delete_' + model))

    # Building HTML list with entities to delete
    ol = _html.Ol()
    for eid in ids:
        entity = dispense_entity(model, eid)
        frm.add_widget(_widget.input.Hidden(name='ids', value=str(entity.id)))
        ol.append(_html.Li(entity.get_d_form_description()))
    frm.add_widget(_widget.static.Text(html_em=_html.Div, title=str(ol)))

    # Action buttons
    submit_button = _widget.button.Submit(weight=10, value=_lang.t('pytsite.odm_ui@delete'), color='danger',
                                          icon='fa fa-save')
    cancel_button_url = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model})
    cancel_button = _widget.button.Link(weight=20, value=_lang.t('pytsite.odm_ui@cancel'), href=cancel_button_url,
                                        icon='fa fa-ban')
    actions_wrapper = _widget.static.Wrapper()
    actions_wrapper.add_child(submit_button).add_child(cancel_button)
    frm.add_widget(actions_wrapper, area='footer')

    return frm


def dispense_entity(model: str, entity_id: str=None):
    """Dispense entity.

    :rtype: _model.UIMixin|odm.model.ODMModel
    """
    if not entity_id or entity_id == '0':
        entity_id = None
    entity = _odm.dispense(model, entity_id)
    if not isinstance(entity, _model.UIMixin):
        raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(model))

    return entity


def check_permissions(perm_type: str, model: str, ids=None) -> bool:
    """Check current user's permissions to operate with entity(es).
    """
    current_user = _auth.get_current_user()

    if current_user.is_anonymous:
        return False

    if type(ids) not in (list, tuple):
        ids = (ids,)

    # Ability for users to modify themselves
    if perm_type == 'modify' and model == 'user' and len(ids) == 1:
        user = _auth.get_user(uid=ids[0])
        if user and user.id == current_user.id:
            return True

    if perm_type == 'create' and current_user.has_permission('pytsite.odm_ui.create.' + model):
        return True
    elif perm_type in ('modify', 'delete'):
        # User can modify or delete ANY entity of this model
        if current_user.has_permission('pytsite.odm_ui.' + perm_type + '.' + model):
            return True

        # User can modify or delete ONLY ITS OWN entity of this model
        else:
            own_perm = 'pytsite.odm_ui.' + perm_type + '_own.' + model
            if _auth.get_permission(own_perm) and current_user.has_permission(own_perm):
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
