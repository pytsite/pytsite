"""Pytsite Form Package.
"""
from typing import Dict as _Dict
from collections import OrderedDict as _OrderedDict
from pytsite import util as _util, widget as _widget, html as _html, router as _router, assetman as _assetman, \
    validation as _validation, tpl as _tpl, events as _events, lang as _lang, ajax as _ajax
from . import _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_lang.register_package(__name__)
_assetman.register_package(__name__)
_assetman.add('pytsite.form@js/form.js', permanent=True)
_tpl.register_package(__name__)
_ajax.register_ep('pytsite.form.ajax.validate')


class Form:
    """Abstract form.
    """
    def __init__(self, uid: str=None, **kwargs):
        """Init.
        """
        if not _router.request():
            raise Exception('Form cannot be created without HTTP request context.')

        # Widgets
        self._widgets = {}  # type: _Dict[str, _widget.Base]

        # Form areas where widgets can be placed
        self._areas = ('hidden', 'header', 'body', 'footer')

        # Areas' CSS classes
        self._area_hidden_css = kwargs.get('area_hidden_css', 'form-area-hidden hidden')
        self._area_header_css = kwargs.get('area_header_css', 'form-area-header box-header')
        self._area_body_css = kwargs.get('area_body_css', 'form-area-body box-body')
        self._area_footer_css = kwargs.get('area_footer_css', 'form-area-footer box-footer')

        self._uid = uid or _util.random_str()
        self._name = kwargs.get('name', '')
        self._method = kwargs.get('method', 'post')
        self._action = kwargs.get('action', '#')
        self._steps = kwargs.get('steps', 1)
        self._modal = kwargs.get('modal', False)

        self._validation_ep = kwargs.get('validation_ep', 'pytsite.form.ajax.validate')
        self._tpl = kwargs.get('tpl', 'pytsite.form@form' if not self._modal else 'pytsite.form@modal-form')

        # <form>'s tag CSS class
        self._css = kwargs.get('css', '') + ' pytsite-form'
        self._css = self._css.strip()

        # Form title
        self._title = kwargs.get('title')
        self._title_css = kwargs.get('title_css', 'box-title')
        self._title_tag = kwargs.get('title_tag', 'h4')

        # Form location
        self.add_widget(_widget.input.Hidden(
            uid='__form_location',
            form_area='hidden',
            value=_router.current_url(),
        ))

        # Form step
        self.add_widget(_widget.input.Hidden(
            uid='__form_steps',
            form_area='hidden',
            value=self.steps,
        ))

        # Form step
        self.add_widget(_widget.input.Hidden(
            uid='__form_step',
            form_area='hidden',
            value=self.step,
        ))

        # Form messages
        self.add_widget(_widget.static.Container(
            uid='__form_messages',
            css='form-messages',
        ))

        # Name is required
        if not self._name:
            self._name = uid

        # 'Actions' area and submit button
        self.add_widget(_widget.static.Container(
            uid='form-actions',
            css='actions-wrapper text-xs-B-center text-sm-left',
            form_area='footer',
        ))
        self.get_widget('form-actions').append(_widget.button.Submit(
            weight=10,
            uid='action-submit',
            value=_lang.t('pytsite.form@save'),
            color='primary', icon='fa fa-save'
        ))

        # Setup hook
        self._setup()

    def _setup(self):
        """_setup() hook.
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
        return self._action

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
    def title_css(self) -> str:
        return self._title_css

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
    def area_body_css(self) -> str:
        return self._area_body_css

    @property
    def area_footer_css(self) -> str:
        return self._area_footer_css

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
        self.get_widget('__form_steps').set_val(value)
        self._steps = value

    @property
    def modal(self) -> bool:
        return self._modal

    @modal.setter
    def modal(self, value: bool):
        self._modal = value

    @property
    def step(self) -> int:
        try:
            return int(_router.request().inp.get('__form_step', 1))
        except ValueError:
            return 1

    @property
    def is_last_step(self) -> bool:
        return self.step == self.steps

    def fill(self, values: dict, **kwargs):
        """Fill form's widgets with values.
        """
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

        # Action adjust
        if not self.is_last_step:
            self._action = _router.current_url()
            self.get_widget('form-actions').get_child('action-submit').value = _lang.t('pytsite.form@next')

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

    def replace_widget(self, uid: str, replacement: _widget.Base):
        """Replace a widget with another one.
        """
        current = self.get_widget(uid)
        if not replacement.weight and current.weight:
            replacement.weight = current.weight

        replacement.form_area = current.form_area

        self.remove_widget(uid).add_widget(replacement)

        return self

    def has_widget(self, uid: str) -> bool:
        """Check if the form has widget.
        """
        return uid in self._widgets

    def get_widget(self, uid: str) -> _widget.Base:
        """Get a widget.
        """
        if not self.has_widget(uid):
            raise KeyError("Widget '{}' is not exists.".format(uid))

        return self._widgets[uid]

    def hide_widget(self, uid):
        """Hide a widget.
        """
        self.get_widget(uid).hide()
        return self

    def get_widgets(self, area: str=None) -> _Dict[str, _widget.Base]:
        """Get widgets.
        """
        widgets = []

        # First, filter widgets by area
        areas = (area,) if area else self._areas
        for area in areas:
            for w in self._widgets.values():
                if w.form_area == area:
                    widgets.append(w)

        # Processing form step information
        for w in widgets:
            if w.form_steps == '*' or (isinstance(w.form_steps, tuple) and self.step in w.form_steps):
                continue

            w.hide()

            # If it isn't first step, try to set hidden widget's value
            # with data received from previous step
            if self.step > 1 and w.uid in _router.request().inp:
                w.value = _router.request().inp[w.uid]

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
