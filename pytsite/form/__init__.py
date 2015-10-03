"""Pytsite Form Package.
"""
from urllib.parse import unquote as _url_unquote
from collections import OrderedDict as _OrderedDict
from pytsite import util as _util, widget as _widget, html as _html, router as _router, assetman as _assetman, \
    validation as _validation, tpl as _tpl

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_assetman.register_package(__name__)
_tpl.register_package(__name__)


class Base:
    """Abstract form.
    """

    def __init__(self, uid: str=None, **kwargs):
        """Init.
        """
        self._widgets = {}
        self._areas = ('hidden', 'header', 'body', 'footer')

        self._uid = uid if uid else _util.random_str()
        self._name = kwargs.get('name', '')
        self._method = kwargs.get('method', 'post')
        self._action = kwargs.get('action', '#')

        self._validation_ep = kwargs.get('validation_ep', 'pytsite.form.ep.validate')
        self._tpl = kwargs.get('tpl', 'pytsite.form@form')

        self._css = kwargs.get('css', '')
        self._css += ' pytsite-form'

        self._title = kwargs.get('title')
        self._title_css = kwargs.get('title_css', 'box-title')
        self._title_tag = kwargs.get('title_tag', 'h3')

        self._area_hidden_css = kwargs.get('area_hidden_css', 'form-area-hidden hidden')
        self._area_header_css = kwargs.get('area_header_css', 'form-area-header box-header')
        self._area_body_css = kwargs.get('area_body_css', 'form-area-body box-body')
        self._area_footer_css = kwargs.get('area_footer_css', 'form-area-footer box-footer')

        redirect_url = _router.request.values_dict.get('__form_redirect')
        if not redirect_url:
            redirect_url = _router.current_url()
        elif isinstance(redirect_url, list):
            redirect_url = redirect_url[0]

        self.add_widget(_widget.input.Hidden(
            uid='__form_location',
            value=_router.current_url(),
            form_area='hidden')
        )
        self.add_widget(_widget.input.Hidden(
            uid='__form_redirect',
            value=_url_unquote(redirect_url),
            form_area='hidden')
        )

        self.add_widget(_widget.static.Wrapper(
            css='form-messages',
            form_area='header',
        ))

        if not self._name:
            self._name = uid

        self._setup()

        # Initializing form JS API
        _assetman.add('pytsite.form@js/form.js')

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
        return _OrderedDict([(w.uid, w.get_value()) for w in self.get_widgets().values()])

    @property
    def fields(self) -> list:
        """Get list of names of all widgets.
        """
        return self.get_widgets().keys()

    @property
    def redirect(self) -> str:
        """Get redirect URL after successful form submit.
        """
        return self.get_widget('__form_redirect').get_value()

    @redirect.setter
    def redirect(self, value):
        """Set redirect URL after successful form submit.
        """
        self.get_widget('__form_redirect').set_value(_url_unquote(value))

    def fill(self, values: dict, **kwargs: dict):
        """Fill form's widgets with values.
        """
        for field_name, field_value in values.items():
            if self.has_widget(field_name):
                self.get_widget(field_name).set_value(field_value, **kwargs)

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
        self.get_widget(widget_uid).remove_rules()

        return self

    def validate(self):
        """Validate the form.
        """
        errors = {}
        # Setting values of the validator
        for widget in self.get_widgets().values():
            try:
                widget.validate()
            except _validation.error.ValidatorError as e:
                for field_name, exception_errors in e.errors.items():
                    if field_name not in errors:
                        errors[field_name] = []
                    for error_msg in exception_errors:
                        errors[field_name].append(error_msg)

        if errors:
            raise _validation.error.ValidatorError(errors)

    def render(self) -> str:
        """Render the form.
        """
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

        replacement.uid = uid
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

    def get_widgets(self, area: str=None):
        """Get widgets.

        :rtype: dict[str, _widget.Base]
        """
        widgets = []

        # Get widgets from area(s) and preparing it for sorting
        areas = (area,) if area else self._areas
        for a in areas:
            for w in self._widgets.values():
                if w.form_area == a:
                    widgets.append(w)

        # Sort by weight
        return _OrderedDict([(w.uid, w) for w in _util.weight_sort(widgets)])

    def remove_widget(self, uid):
        """Remove widget from the form.
        """
        if uid in self._widgets:
            del self._widgets[uid]

        return self

    def render_widget(self, widget_uid: str) -> _html.Element:
        """Render form's widget.
        """
        return self.get_widget(widget_uid).render()
