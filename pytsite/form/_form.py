"""PytSite Base Form.
"""
from typing import Dict as _Dict
from collections import OrderedDict as _OrderedDict
from pytsite import util as _util, widget as _widget, html as _html, router as _router, validation as _validation, \
    tpl as _tpl, events as _events, lang as _lang, assetman as _assetman
from . import _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form:
    """Base Form.
    """
    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        if not _router.request():
            raise RuntimeError('Form cannot be created without HTTP request context.')

        self._widgets_added = False

        # Widgets
        self._widgets = {}  # type: _Dict[str, _widget.Base]

        # Form areas where widgets can be placed
        self._areas = ('hidden', 'header', 'body', 'footer')

        # Areas CSS classes
        self._area_hidden_css = kwargs.get('area_hidden_css', '')
        self._area_header_css = kwargs.get('area_header_css', '')
        self._area_body_css = kwargs.get('area_body_css', '')
        self._area_footer_css = kwargs.get('area_footer_css', '')

        # Messages area CSS
        self._messages_css = kwargs.get('messages_css', 'form-messages')

        self._uid = uid or _util.md5_hex_digest(self.cid)
        self._name = kwargs.get('name') or self._uid
        self._method = kwargs.get('method', 'post')
        self._action = kwargs.get('action', '#')
        self._steps = kwargs.get('steps', 1)
        self._step = kwargs.get('step', 1)
        self._modal = kwargs.get('modal', False)
        self._reload_on_forward = kwargs.get('reload_on_forward', False)

        # Redirect info
        if '__redirect' in _router.request().inp:
            self._redirect = _router.request().inp['__redirect']
        else:
            self._redirect = kwargs.get('redirect')

        # AJAX endpoint to load form's widgets
        self._get_widgets_ep = kwargs.get('get_widgets_ep', 'pytsite.form.ajax.get_widgets')

        # AJAX endpoint to perform form validation
        self._validation_ep = kwargs.get('validation_ep', 'pytsite.form.ajax.validate')

        # Form template
        self._tpl = kwargs.get('tpl', 'pytsite.form@form')

        # <form>'s tag CSS class
        self._css = kwargs.get('css', '') + ' pytsite-form'
        self._css = self._css.strip()

        # Title
        self._title = kwargs.get('title')
        self._title_css = kwargs.get('title_css', 'box-title')

        self._data = kwargs.get('data', {})

        # Convert kwargs to data-attributes. It is convenient method to export additional form constructor's arguments
        # in child classes. It is necessary to pass arguments back via AJAX requests when validating forms.
        skip_data_kwargs = ('area_hidden_css', 'area_header_css', 'area_body_css', 'area_footer_css', 'messages_css',
                            'name', 'method', 'action', 'modal', 'tpl', 'css', 'title', 'redirect')
        for k, v in kwargs.items():
            if k not in skip_data_kwargs:
                if isinstance(v, (tuple, list)):
                    v = ','.join(v)
                self._data.update({k: v})

        # 'Submit' button for the last step
        self.add_widget(_widget.button.Submit(
            weight=20,
            uid='action-submit',
            value=_lang.t('pytsite.form@save'),
            color='primary',
            icon='fa fa-save',
            form_area='footer',
            css='form-action-submit',
        ))

        # Assets
        _assetman.add('pytsite.form@css/form.css')
        _assetman.add('pytsite.form@js/form.js')

        # Setup hook
        self._setup_form()

    def _setup_form(self):
        """Hook.
        """
        pass

    def _setup_widgets(self):
        """Hook.
        """
        pass

    @property
    def areas(self) -> tuple:
        """Get form's areas.
        """
        return self._areas

    @property
    def uid(self) -> str:
        """Get form ID.
        """
        return self._uid

    @property
    def cid(self) -> str:
        """Class ID.
        """
        return '{}.{}'.format(self.__module__, self.__class__.__name__)

    @property
    def name(self) -> str:
        """Get form name.
        """
        return self._name

    @property
    def method(self) -> str:
        """Get method.
        """
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def action(self) -> str:
        """Get form action URL.
        """
        r = self._action
        if self._redirect:
            r = _router.url(r, query={'__redirect': self._redirect})

        return r

    @action.setter
    def action(self, value):
        """Set form action URL.
        """
        self._action = value

    @property
    def title(self) -> str:
        """Get title.
        """
        return self._title

    @title.setter
    def title(self, value: str):
        """Set title.
        """
        self._title = value

    @property
    def css(self) -> str:
        """Get CSS classes.
        """
        return self._css

    @css.setter
    def css(self, value):
        """Set CSS classes.
        """
        self._css = value + ' pytsite-form'

    @property
    def area_hidden_css(self) -> str:
        return self._area_hidden_css

    @property
    def area_header_css(self) -> str:
        return self._area_header_css

    @property
    def title_css(self) -> str:
        return self._title_css

    @property
    def messages_css(self) -> str:
        return self._messages_css

    @property
    def area_body_css(self) -> str:
        return self._area_body_css

    @property
    def area_footer_css(self) -> str:
        return self._area_footer_css

    @property
    def get_widgets_ep(self) -> str:
        return self._get_widgets_ep

    @get_widgets_ep.setter
    def get_widgets_ep(self, val: str):
        self._get_widgets_ep = val

    @property
    def validation_ep(self) -> str:
        """Get validation endpoint.
        """
        return self._validation_ep

    @validation_ep.setter
    def validation_ep(self, value):
        """Set validation endpoint.
        """
        self._validation_ep = value

    @property
    def values(self) -> dict:
        return _OrderedDict([(w.uid, w.get_val()) for w in self.get_widgets().values()])

    @property
    def fields(self) -> list:
        """Get list of names of all widgets.
        """
        return self.get_widgets().keys()

    @property
    def steps(self) -> int:
        return self._steps

    @steps.setter
    def steps(self, value: int):
        self._steps = value

    @property
    def step(self) -> int:
        return self._step

    @step.setter
    def step(self, value: int):
        self._step = value

    @property
    def modal(self) -> bool:
        return self._modal

    @modal.setter
    def modal(self, value: bool):
        self._modal = value

    @property
    def reload_on_forward(self) -> bool:
        return self._reload_on_forward

    @reload_on_forward.setter
    def reload_on_forward(self, val: bool):
        self._reload_on_forward = val

    @property
    def redirect(self) -> str:
        return self._redirect

    @redirect.setter
    def redirect(self, val: str):
        self._redirect = val

    @property
    def data(self) -> dict:
        return self._data

    def fill(self, values: dict, **kwargs):
        """Fill form's widgets with values.
        """
        self.setup_widgets()

        for field_name, field_value in values.items():
            if self.has_widget(field_name):
                self.get_widget(field_name).set_val(field_value, **kwargs)

        return self

    def add_rule(self, widget_uid: str, rule: _validation.rule.Base):
        """Add a rule to the widget.
        """
        self.get_widget(widget_uid).add_rule(rule)

        return self

    def add_rules(self, widget_uid: str, rules: tuple):
        """Add multiple rules to the widgets.
        """
        for rule in rules:
            self.add_rule(widget_uid, rule)

        return self

    def remove_rules(self, widget_uid: str):
        """Remove validation's rules from the widget.
        """
        self.get_widget(widget_uid).clr_rules()

        return self

    def validate(self):
        """Validate the form.
        """
        errors = {}

        # Validate each widget
        for f_name, widget in self.get_widgets().items():
            try:
                widget.validate()
            except _validation.error.RuleError as e:
                if f_name not in errors:
                    errors[f_name] = []
                errors[f_name].append(str(e))

        if errors:
            raise error.ValidationError(errors)

    def render(self) -> str:
        """Render the form.
        """
        _events.fire('pytsite.form.render.' + self.uid.replace('-', '_'), frm=self)

        return _tpl.render(self._tpl, {'form': self})

    def __str__(self) -> str:
        """Render the form.
        """
        return self.render()

    def add_widget(self, widget: _widget.Base):
        """Add a widget.
        """
        if widget.form_area not in self._areas:
            raise ValueError("Invalid form area: '{}'".format(widget.form_area))

        if widget.uid in self._widgets:
            raise KeyError("Widget '{}' is already added.".format(widget.uid))

        self._widgets[widget.uid] = widget

        return self

    def replace_widget(self, source_uid: str, replacement: _widget.Base):
        """Replace a widget with another one.
        """
        current = self.get_widget(source_uid)
        if not replacement.weight and current.weight:
            replacement.weight = current.weight

        replacement.form_area = current.form_area
        replacement.replaces = source_uid

        self.remove_widget(source_uid).add_widget(replacement)

        return self

    def has_widget(self, uid: str) -> bool:
        """Check if the form has widget.
        """
        return uid in self._widgets

    def get_widget(self, uid: str) -> _widget.Base:
        """Get a widget.
        """
        if not self.has_widget(uid):
            raise KeyError("Widget '{}' does not exist.".format(uid))

        return self._widgets[uid]

    def hide_widget(self, uid):
        """Hide a widget.
        """
        self.get_widget(uid).hide()

        return self

    def get_widgets(self, area: str = None, step: int = None) -> _Dict[str, _widget.Base]:
        """Get widgets.
        """
        self.setup_widgets()

        widgets = []

        # First, filter widgets by area
        for w in self._widgets.values():
            # Filter by area
            if area and w.form_area != area:
                continue

            # Filter by step
            if step and step != w.form_step:
                continue

            widgets.append(w)

        # Sort by weight
        return _OrderedDict([(w.uid, w) for w in _util.weight_sort(widgets)])

    def remove_widget(self, widget_uid: str):
        """Remove widget from the form.
        """
        if widget_uid in self._widgets:
            self.remove_rules(widget_uid)
            del self._widgets[widget_uid]

        return self

    def render_widget(self, widget_uid: str) -> _html.Element:
        """Render form's widget.
        """
        return self.get_widget(widget_uid).get_html_em()

    def setup_widgets(self):
        """Ensures that widgets is added.
        """
        if self._widgets_added:
            return self

        self._setup_widgets()

        if self._steps > 1:
            # Submit button appears only on the last step
            self.get_widget('action-submit').form_step = self.steps

            # 'Next' button for all steps except the last one
            for i in range(1, self._steps):
                self.add_widget(_widget.button.Submit(
                    weight=20,
                    uid='action-forward-' + str(i + 1),
                    value=_lang.t('pytsite.form@forward'),
                    form_area='footer',
                    form_step=i,
                    color='primary',
                    icon='fa fa-forward',
                    css='form-action-forward',
                    data={
                        'to-step': i + 1,
                    }
                ))

            # 'Back' button for all steps except the first one
            for i in range(2, self._steps + 1):
                self.add_widget(_widget.button.Button(
                    weight=10,
                    uid='action-backward-' + str(i - 1),
                    value=_lang.t('pytsite.form@backward'),
                    form_area='footer',
                    form_step=i,
                    icon='fa fa-backward',
                    css='form-action-backward',
                    data={
                        'to-step': i - 1,
                    }
                ))

        self._widgets_added = True

        return self
