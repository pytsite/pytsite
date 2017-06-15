"""PytSite Base Form.
"""
import re as _re
from typing import List as _List
from abc import ABC as _ABC
from collections import OrderedDict as _OrderedDict
from datetime import datetime as _datetime
from pytsite import util as _util, widget as _widget, router as _router, validation as _validation, tpl as _tpl, \
    events as _events, lang as _lang, assetman as _assetman
from . import _error, _cache

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_form_name_sub_re = _re.compile('[._]+')


class Form(_ABC):
    """Base Form.
    """

    def __init__(self, **kwargs):
        """Init.
        """
        if not _router.request():
            raise RuntimeError('Form cannot be created without HTTP request context.')

        # Widgets
        self._widgets = []  # type: _List[_widget.Abstract]

        # Form areas where widgets can be placed
        self._areas = ('hidden', 'header', 'body', 'footer')

        # Areas CSS classes
        self._area_hidden_css = kwargs.get('area_hidden_css', '')
        self._area_header_css = kwargs.get('area_header_css', '')
        self._area_body_css = kwargs.get('area_body_css', '')
        self._area_footer_css = kwargs.get('area_footer_css', '')

        # Messages CSS
        self._messages_css = kwargs.get('messages_css', 'form-messages')

        self._uid = kwargs.get('uid', _util.random_str(64))
        self._created = _datetime.now()
        self._name = kwargs.get('name') or _form_name_sub_re.sub('-', self.cid.lower())
        self._path = kwargs.get('path', _router.current_path(True))
        self._method = kwargs.get('method', 'post')
        self._action = kwargs.get('action', _router.rule_url('pytsite.form@submit', {'uid': self.uid}))
        self._steps = int(kwargs.get('steps', 1))
        self._step = int(kwargs.get('step', 1))
        self._modal = kwargs.get('modal', False)
        self._modal_close_btn = kwargs.get('modal_close_btn', True)
        self._prevent_submit = kwargs.get('prevent_submit', False)
        self._redirect = _router.request().inp.get('__redirect', kwargs.get('redirect'))
        self._nocache = kwargs.get('nocache', False)

        # AJAX endpoint to load form's widgets
        self._get_widgets_ep = kwargs.get('get_widgets_ep', 'form/widgets')

        # AJAX endpoint to perform form validation
        self._validation_ep = kwargs.get('validation_ep', 'form/validate')

        # Form template
        self._tpl = kwargs.get('tpl', 'pytsite.form@form')

        # <form>'s tag CSS class
        self._css = str(kwargs.get('css', '') + ' pytsite-form').strip()
        self._css += ' form-name-{} form-cid-{}'.format(self._name, _form_name_sub_re.sub('-', self.cid.lower()))

        # Title
        self._title = kwargs.get('title')
        self._title_css = kwargs.get('title_css', 'box-title')

        self._data = kwargs.get('data', {})

        # Convert kwargs to data-attributes. It is convenient method to export additional form constructor's arguments
        # in child classes. It is necessary to pass arguments back via AJAX requests when validating forms.
        skip_data_kwargs = ('area_hidden_css', 'area_header_css', 'area_body_css', 'area_footer_css', 'messages_css',
                            'name', 'path', 'method', 'action', 'steps', 'step', 'modal', 'modal_close_btn',
                            'prevent_submit', 'redirect', 'nocache', 'get_widgets_ep', 'validation_ep', 'tpl', 'css',
                            'title', 'title_css', 'data')
        for k, v in kwargs.items():
            if k not in skip_data_kwargs:
                if isinstance(v, (tuple, list)):
                    v = ','.join(v)
                self._data.update({k: v})

        # Assets
        _assetman.preload('pytsite.form@css/form.css')
        _assetman.preload('pytsite.form@js/index.js')

        # Setup form
        self._on_setup_form(**kwargs)

        # Put form into the cache
        if not self._nocache:
            _cache.put(self)

    def setup_widgets(self, remove_existing: bool = True):
        """Setup form's widgets.
        """
        # Remove all previously added widgets
        if remove_existing:
            self.remove_widgets()

        # 'Submit' button for the last step
        if self._steps == self._step:
            self.add_widget(_widget.button.Submit(
                weight=20,
                uid='action-submit',
                value=_lang.t('pytsite.form@save'),
                color='primary',
                icon='fa fa-fw fa-save',
                form_area='footer',
                css='form-action-submit',
            ))

        # 'Next' button for all steps except the last one
        if self._step < self._steps:
            self.add_widget(_widget.button.Submit(
                weight=20,
                uid='action-forward-' + str(self._step + 1),
                value=_lang.t('pytsite.form@forward'),
                form_area='footer',
                color='primary',
                icon='fa fa-fw fa-forward',
                css='form-action-forward',
                data={
                    'to-step': self._step + 1,
                }
            ))

        # 'Back' button for all steps except the first one
        if self._step > 1:
            self.add_widget(_widget.button.Button(
                weight=10,
                uid='action-backward-' + str(self._step - 1),
                value=_lang.t('pytsite.form@backward'),
                form_area='footer',
                form_step=self._step,
                icon='fa fa-fw fa-backward',
                css='form-action-backward',
                data={
                    'to-step': self._step - 1,
                }
            ))

        self._on_setup_widgets()

        _events.fire('pytsite.form.setup_widgets.' + self.uid.replace('-', '_'), frm=self)

    def _on_setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        pass

    def _on_setup_widgets(self):
        """Hook.
        """
        pass

    def _on_validate(self):
        """Hook.
        """
        pass

    def _on_submit(self):
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

    @uid.setter
    def uid(self, value: str):
        """Set form uid.
        """
        self._uid = value

    @property
    def created(self) -> _datetime:
        return self._created

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

    @name.setter
    def name(self, value: str):
        """Set form name.
        """
        self._name = value

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
        return _router.url(self._action, query={'__redirect': self._redirect}) if self._redirect else self._action

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
        self._css = value + ' pytsite-form' if 'pytsite-form' not in value else value

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

    @area_body_css.setter
    def area_body_css(self, value: str):
        self._area_body_css = value

    @property
    def area_footer_css(self) -> str:
        return self._area_footer_css

    @area_footer_css.setter
    def area_footer_css(self, value: str):
        self._area_footer_css = value

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
    def values(self) -> _OrderedDict:
        return _OrderedDict([(w.name, w.get_val()) for w in self.get_widgets()])

    @property
    def fields(self) -> list:
        """Get list of names of all widgets.
        """
        return [w.uid for w in self.get_widgets()]

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
    def modal_close_btn(self) -> bool:
        return self._modal_close_btn

    @modal_close_btn.setter
    def modal_close_btn(self, value: bool):
        self._modal_close_btn = value

    @property
    def prevent_submit(self) -> bool:
        return self._prevent_submit

    @prevent_submit.setter
    def prevent_submit(self, val: bool):
        self._prevent_submit = val

    @property
    def redirect(self) -> str:
        return self._redirect

    @redirect.setter
    def redirect(self, val: str):
        self._redirect = val

    @property
    def data(self) -> dict:
        return self._data

    @property
    def path(self) -> str:
        return self._path

    @property
    def nocache(self) -> bool:
        return self. _nocache

    @nocache.setter
    def nocache(self, value: bool):
        self._nocache = value

    def fill(self, values: dict, **kwargs):
        """Fill form's widgets with values.
        """
        for widget in self.get_widgets():
            if widget.name in values:
                widget.set_val(values[widget.name], **kwargs)

        return self

    def add_rule(self, widget_uid: str, rule: _validation.rule.Rule):
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
        for w in self.get_widgets():
            try:
                w.validate()
            except _validation.error.RuleError as e:
                if w.uid not in errors:
                    errors[w.uid] = []
                errors[w.uid].append(str(e))

        if errors:
            raise _error.ValidationError(errors)

        self._on_validate()

        return self

    def submit(self):
        """Should be called by endpoint when it processing form submit.
         """
        response = self._on_submit()

        # Remove submitted form from the cache
        if not self.nocache:
            _cache.rm(self.uid)

        return response

    def render(self) -> str:
        """Render the form.
        """
        _events.fire('pytsite.form.render.' + self.uid.replace('-', '_'), frm=self)

        return _tpl.render(self._tpl, {'form': self})

    def __str__(self) -> str:
        """Render the form.
        """
        return self.render()

    def add_widget(self, widget: _widget.Abstract):
        """Add a widget.
        """
        if widget.form_area not in self._areas:
            raise ValueError("Invalid form area: '{}'".format(widget.form_area))

        if widget.uid in self._widgets:
            raise KeyError("Widget '{}' is already added.".format(widget.uid))

        self._widgets.append(widget)
        self._widgets.sort(key=lambda x: x.weight)

        return self

    def replace_widget(self, source_uid: str, replacement: _widget.Abstract):
        """Replace a widget with another one.
        """
        current = self.get_widget(source_uid)
        if not replacement.weight and current.weight:
            replacement.weight = current.weight

        replacement.form_area = current.form_area
        replacement.replaces = source_uid

        self.remove_widget(source_uid).add_widget(replacement)

        return self

    def hide_widget(self, uid):
        """Hide a widget.
         """
        self.get_widget(uid).hide()

        return self

    def get_widgets(self, filter_by: str = None, filter_val=None, _parent: _widget.Abstract = None):
        """Get widgets.

        :rtype: _List[_widget.Abstract]
        """
        r = []

        # Recursion depth > 0
        if _parent:
            # Filter by some widget's attribute
            if not filter_by or (filter_by and getattr(_parent, filter_by) == filter_val):
                r.append(_parent)

            try:
                for widget in _parent.children:
                    r += self.get_widgets(filter_by, filter_val, widget)
            except NotImplementedError:
                pass

        # Recursion depth == 0
        else:
            for widget in self._widgets:
                r += self.get_widgets(filter_by, filter_val, widget)

        return r

    def get_widget(self, uid: str) -> _widget.Abstract:
        """Get a widget.
        """
        r = self.get_widgets(filter_by='uid', filter_val=uid)
        if not r:
            raise _error.WidgetNotExist("Widget '{}' does not exist.".format(uid))

        return r[0]

    def has_widget(self, uid: str) -> bool:
        """Check if the form has widget.
        """
        try:
            self.get_widget(uid)
            return True
        except _error.WidgetNotExist:
            return False

    def remove_widget(self, uid: str):
        """Remove widget from the form.
        """
        w = self.get_widget(uid)
        w.clr_rules()

        if w.parent:
            w.parent.remove_child(uid)
        else:
            self._widgets = [w for w in self._widgets if w.uid != uid]

        return self

    def remove_widgets(self):
        """Remove all added widgets.
        """
        self._widgets = []

        return self
