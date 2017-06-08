"""PytSite ODM Entity Modify Form.
"""
from pytsite import form as _form, widget as _widget, lang as _lang, http as _http, odm as _odm, events as _events, \
    metatag as _metatag, router as _router, html as _html, odm_auth as _odm_auth, logger as _logger, errors as _errors
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Modify(_form.Form):
    def __init__(self, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._eid = kwargs.get('eid')
        self._update_meta_title = kwargs.get('update_meta_title', True)

        super().__init__(**kwargs)

    @property
    def update_meta_title(self) -> bool:
        return self._update_meta_title

    @update_meta_title.setter
    def update_meta_title(self, value: bool):
        self._update_meta_title = value

    def _on_setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        from ._api import dispense_entity

        try:
            entity = dispense_entity(self._model, self._eid)
        except _odm.error.EntityNotFound:
            raise _http.error.NotFound()

        # Check if entities of this model can be created

        if entity.is_new:
            perms_allow = entity.odm_auth_check_permission('create')
            odm_ui_allows = entity.odm_ui_creation_allowed()
            if not (perms_allow and odm_ui_allows):
                raise _http.error.Forbidden()

        # Check if the entity can be modified
        if not entity.is_new:
            perms_allow = entity.odm_auth_check_permission('modify') or entity.odm_auth_check_permission('modify_own')
            odm_ui_allows = entity.odm_ui_modification_allowed()
            if not (perms_allow and odm_ui_allows):
                raise _http.error.Forbidden()

        # Form title
        if entity.is_new:
            self._title = entity.t('odm_ui_form_title_create_' + self._model)
        else:
            self._title = entity.t('odm_ui_form_title_modify_' + self._model)

        # Setting up the form through entity hook and global event
        entity.odm_ui_m_form_setup(self)
        _events.fire('pytsite.odm_ui.{}.m_form_setup'.format(self._model), frm=self, entity=entity)

        if self._update_meta_title:
            _metatag.t_set('title', self.title)

        # Default redirect
        if not self._redirect:
            self._redirect = 'ENTITY_VIEW'

        # CSS
        self.css += ' odm-ui-form odm-ui-form-' + self._model

    def _on_setup_widgets(self):
        from ._api import dispense_entity

        # Setting up form's widgets through entity hook and global event
        entity = dispense_entity(self._model, self._eid)
        entity.odm_ui_m_form_setup_widgets(self)
        _events.fire('pytsite.odm_ui.{}.m_form_setup_widgets'.format(self._model), frm=self, entity=entity)

        if self.step == 1:
            # Entity model
            self.add_widget(_widget.input.Hidden(
                uid='model',
                value=self._model,
                form_area='hidden',
            ))

            # Entity ID
            self.add_widget(_widget.input.Hidden(
                uid='eid',
                value=self._eid,
                form_area='hidden',
            ))

        # Cancel button
        cancel_href = '#'
        if not self.modal:
            cancel_href = _router.request().inp.get('__redirect')
            if not cancel_href or cancel_href == 'ENTITY_VIEW':
                if not entity.is_new and entity.odm_ui_view_url():
                    cancel_href = entity.odm_ui_view_url()
                else:
                    cancel_href = _router.base_url()

        self.add_widget(_widget.button.Link(
            weight=15,
            uid='action-cancel-' + str(self.step),
            value=_lang.t('pytsite.odm_ui@cancel'),
            icon='fa fa-fw fa-remove',
            href=cancel_href,
            dismiss='modal',
            form_area='footer',
        ))

    def _on_validate(self):
        # Ask entity to validate the form
        from ._api import dispense_entity

        dispense_entity(self._model, self._eid).odm_ui_m_form_validate(self)

    def _on_submit(self):
        from ._api import dispense_entity

        # Dispense entity
        entity = dispense_entity(self._model, self._eid)

        # Fill entity fields
        with entity:
            # Let entity know about form submission
            entity.odm_ui_m_form_submit(self)

            # Populate form values to entity
            for f_name, f_value in self.values.items():
                if entity.has_field(f_name):
                    entity.f_set(f_name, f_value)

            try:
                # Save entity
                entity.save()
                _router.session().add_info_message(_lang.t('pytsite.odm_ui@operation_successful'))

            except Exception as e:
                _router.session().add_error_message(str(e))
                _logger.error(str(e), exc_info=e, stack_info=True)
                raise e

        # Process 'special' redirect endpoint
        if self.redirect == 'ENTITY_VIEW':
            self.redirect = entity.odm_ui_view_url()

        return _http.response.Redirect(self.redirect)


class MassAction(_form.Form):
    """ODM UI Mass Action Form.
    """

    def __init__(self, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._eids = kwargs.get('eids')
        if isinstance(self._eids, str):
            self._eids = self._eids.split(',')

        super().__init__(**kwargs)

    def _on_setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        if not self._redirect:
            self._redirect = _router.ep_url('pytsite.odm_ui@browse', {'model': self._model})

    def _on_setup_widgets(self):
        """Hook.
        """
        from ._api import dispense_entity

        # List of items to process
        ol = _html.Ol()
        for eid in self._eids:
            entity = dispense_entity(self._model, eid)
            self.add_widget(_widget.input.Hidden(uid='ids-' + eid, name='ids', value=eid))
            ol.append(_html.Li(entity.odm_ui_mass_action_entity_description()))
        self.add_widget(_widget.static.HTML(uid='ids-text', em=ol))

        # Submit button
        submit_button = self.get_widget('action-submit')  # type: _widget.button.Submit
        submit_button.value = _lang.t('pytsite.odm_ui@continue')
        submit_button.icon = 'angle-double-right'

        # Cancel button
        self.add_widget(_widget.button.Link(
            uid='action-cancel',
            weight=10,
            value=_lang.t('pytsite.odm_ui@cancel'),
            href=self.redirect,
            icon='fa fa-fw fa-ban',
            form_area='footer'
        ))


class Delete(MassAction):
    """Entities Delete Form.
    """

    def _on_setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        super()._on_setup_form()

        # Check permissions
        for eid in self._eids:
            if not (_odm_auth.check_permission('delete', self._model) or
                    _odm_auth.check_permission('delete_own', self._model, eid)):
                raise _http.error.Forbidden()

        # Page title
        model_class = _odm.get_model_class(self._model)  # type: _model.UIEntity
        _metatag.t_set('title', model_class.t('odm_ui_form_title_delete_' + self._model))

    def _on_setup_widgets(self):
        """Hook.
        """
        super()._on_setup_widgets()

        # Change submit button color
        self.get_widget('action-submit').color = 'danger'

    def _on_submit(self):
        from ._api import dispense_entity

        try:
            # Delete entities
            for eid in self._eids:
                dispense_entity(self._model, eid).odm_ui_d_form_submit()

            _router.session().add_info_message(_lang.t('pytsite.odm_ui@operation_successful'))

        # Entity deletion was forbidden
        except _errors.ForbidDeletion as e:
            _logger.error(str(e), exc_info=e)
            _router.session().add_error_message(_lang.t('pytsite.odm_ui@entity_deletion_forbidden') + '. ' + str(e))

        default_redirect = _router.ep_url('pytsite.odm_ui@browse', {'model': self._model})

        return _http.response.Redirect(_router.request().inp.get('__redirect', default_redirect))
