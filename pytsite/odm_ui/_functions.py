"""ODM UI Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import auth as _auth
from pytsite.core import router as _router, metatag as _metatag, odm as _odm, lang as _lang, http as _http, \
    form as _form, widget as _widget, html as _html

from . import _model


def get_m_form(model: str, eid: str=None, stage: str='show') -> _form.Base:
    """Get entity modification _form.
    """
    eid = eid if eid != '0' else None

    if not eid and not _check_permissions('create', model):
        raise _http.error.ForbiddenError()
    elif eid and not _check_permissions('modify', model, [eid]):
        raise _http.error.ForbiddenError()

    frm = _form.Base('odm-ui-form')
    frm.cls += ' odm-ui-form odm-ui-form-' + model

    # Action, redirect and validation endpoints
    frm.validation_ep = 'pytsite.odm_ui.eps.validate_m_form'
    frm.action = _router.endpoint_url('pytsite.odm_ui.eps.post_m_form', {'model': model, 'id': eid if eid else '0'})
    frm.redirect = _router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})

    # Action buttons
    submit_button = _widget.button.Submit(weight=10, uid='action_submit', value=_lang.t('pytsite.odm_ui@save'),
                                          color='primary', icon='fa fa-save')
    cancel_button_url = _router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    cancel_button = _widget.button.Link(weight=20, uid='action_cancel', value=_lang.t('pytsite.odm_ui@cancel'),
                                        href=cancel_button_url, icon='fa fa-remove')
    actions_wrapper = _widget.static.Wrapper(uid='actions',
                                             cls='actions-wrapper text-xs-B-center text-sm-left')
    actions_wrapper.add_child(submit_button).add_child(cancel_button)
    frm.add_widget(actions_wrapper, area='footer')

    # Metadata
    frm.add_widget(_widget.input.Hidden(uid='__model', value=model), area='form')
    frm.add_widget(_widget.input.Hidden(uid='__entity_id', value=eid), area='form')

    # Setting up the form with entity hook
    entity = dispense_entity(model, eid)
    entity.setup_m_form(frm, stage)

    if entity.is_new:
        legend = entity.t('odm_ui_' + model + '_create_form_legend')
    else:
        legend = entity.t('odm_ui_' + model + '_modify_form_legend')

    _metatag.t_set('title', legend)

    return frm


def get_d_form(model: str, ids: list) -> _form.Base:
    """Get entities delete _form.
    """
    if not _check_permissions('delete', model, ids):
        raise _http.error.ForbiddenError()

    frm = _form.Base('odm-ui-delete-form')
    frm.action = _router.endpoint_url('pytsite.odm_ui.eps.post_d_form', {'model': model})
    ol = _html.Ol()

    mock = dispense_entity(model)
    _metatag.t_set('title', mock.t('odm_ui_' + model + '_delete_form_legend'))

    for eid in ids:
        entity = dispense_entity(model, eid)
        frm.add_widget(_widget.input.Hidden(name='ids', value=str(entity.id)))
        ol.append(_html.Li(entity.get_d_form_description()))

    frm.add_widget(_widget.static.Text(html_em=_html.Div, value=str(ol)))

    # Action buttons
    submit_button = _widget.button.Submit(weight=10, value=_lang.t('pytsite.odm_ui@delete'), color='danger', icon='fa fa-save')
    cancel_button_url = _router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    cancel_button = _widget.button.Link(weight=20, value=_lang.t('pytsite.odm_ui@cancel'), href=cancel_button_url, icon='fa fa-ban')
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


def _check_permissions(perm_type: str, model: str, ids=None) -> bool:
    user = _auth.get_current_user()

    if user.is_anonymous():
        return False

    if perm_type == 'create' and user.has_permission('pytsite.odm_ui.create.' + model):
        return True
    elif perm_type == 'modify' or perm_type == 'delete':
        if user.has_permission('pytsite.odm_ui.' + perm_type + '.' + model):
            return True
        elif user.has_permission('pytsite.odm_ui.' + perm_type + '_own.' + model):
            for eid in ids:
                entity = dispense_entity(model, eid)
                if not entity:
                    return False
                if entity.has_field('author') and not entity.f_get('author').id == user.id:
                    return False
                if entity.has_field('owner') and not entity.f_get('owner').id == user.id:
                    return False
            return True

    return False
