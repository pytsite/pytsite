"""PytSite ODM Entity Modify Form.
"""
from pytsite import form as _form, widget as _widget, lang as _lang, http as _http, odm as _odm, events as _events, \
    metatag as _metatag, router as _router, html as _html
from . import _entity

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Modify(_form.Form):
    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._eid = kwargs.get('eid')
        self._update_meta_title = kwargs.get('update_meta_title', True)

        super().__init__(uid, **kwargs)

    def setup(self):
        """Hook.
        """
        from ._api import check_permissions, dispense_entity

        # Default redirect
        self._redirect = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': self._model})

        # Checking 'create' permission
        if not self._eid and not check_permissions('create', self._model):
            raise _http.error.Forbidden()

        # Checking 'modify' permission
        if self._eid and not check_permissions('modify', self._model, self._eid):
            raise _http.error.Forbidden()

        # Checking model-wide permissions
        model_class = _odm.get_model_class(self._model)  # type: _entity.UIEntity
        if not self._eid and not model_class.ui_model_creation_enabled():
            raise _http.error.Forbidden()
        if self._eid and not model_class.ui_model_modification_enabled():
            raise _http.error.Forbidden()

        # Dispense entity
        entity = dispense_entity(self._model, self._eid)

        # Form title
        if entity.is_new:
            self._title = entity.t('odm_ui_form_title_create_' + self._model)
        else:
            self._title = entity.t('odm_ui_form_title_modify_' + self._model)

        if self._update_meta_title:
            _metatag.t_set('title', self.title)

        # Setting up the form through entity hook
        entity.ui_m_form_setup(self)
        _events.fire('pytsite.odm_ui.{}.m_form_setup'.format(self._model), frm=self, entity=entity)

        # Action URL
        self._action = _router.ep_url('pytsite.odm_ui.ep.m_form_submit', {
            'model': self._model,
            'id': self._eid or '0',
        })

        # Cancel button
        self.add_widget(_widget.button.Link(
            weight=30,
            uid='action-cancel',
            value=_lang.t('pytsite.odm_ui@cancel'),
            icon='fa fa-remove',
            href=self._redirect if not self.modal else '#',
            dismiss='modal',
            form_area='footer',
        ))

        # CSS
        self.css += ' odm-ui-form odm-ui-form-' + self._model


class MassAction(_form.Form):
    """ODM UI Mass Action Form.
    """
    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._eids = kwargs.get('eids')
        if isinstance(self._eids, str):
            self._eids = self._eids.split(',')

        super().__init__(uid, **kwargs)

    def setup(self):
        """Hook.
        """
        from ._api import dispense_entity

        # List of items to process
        ol = _html.Ol()
        for eid in self._eids:
            entity = dispense_entity(self._model, eid)
            self.add_widget(_widget.input.Hidden(uid='ids-' + eid, name='ids', value=eid))
            ol.append(_html.Li(entity.ui_mass_action_get_entity_description()))
        self.add_widget(_widget.static.HTML(uid='ids-text', em=ol))

        # Redirect after successful form submit
        self._redirect = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': self._model})

        # Submit button
        submit_button = self.get_widget('action-submit')  # type: _widget.button.Submit
        submit_button.value = _lang.t('pytsite.odm_ui@continue')
        submit_button.icon = 'angle-double-right'

        # Cancel button
        self.add_widget(_widget.button.Link(
            uid='action-cancel',
            weight=30,
            value=_lang.t('pytsite.odm_ui@cancel'),
            href=self.redirect,
            icon='ban',
            form_area='footer'
        ))


class Delete(MassAction):
    """Entities Delete Form.
    """
    def setup(self):
        """Hook.
        """
        from ._api import check_permissions

        super().setup()

        model_class = _odm.get_model_class(self._model)  # type: _entity.UIEntity

        # Check permissions
        if not check_permissions('delete', self._model, self._eids) or not model_class.ui_model_deletion_enabled():
            raise _http.error.Forbidden()

        # Action URL
        self._action = _router.ep_url('pytsite.odm_ui.ep.d_form_submit', {'model': self._model})

        # Change submit button color
        self.get_widget('action-submit').color = 'danger'

        # Page title
        _metatag.t_set('title', model_class.t('odm_ui_form_title_delete_' + self._model))
