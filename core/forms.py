"""Forms.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from .util import xml_attrs_str, dict_sort
from .widgets.abstract import AbstractWidget
from .widgets.input import HiddenInputWidget
from .widgets.wrapper import WrapperWidget
from .widgets.static import HtmlWidget
from .validation.validator import Validator
from .validation.rules import BaseRule
from .html import Div, H3
from . import router, assetman


class BaseForm:
    """Abstract form.
    """

    def __init__(self, uid: str, **kwargs: dict):
        """Init.
        """

        self._uid = uid
        self._name = kwargs.get('name', None)
        self._method = kwargs.get('method', 'post')
        self._action = kwargs.get('action', '#')
        self._legend = kwargs.get('legend', None)
        self._cls = kwargs.get('cls', 'pytsite-form')
        self._validation_ep = kwargs.get('validation_ep')

        self._areas = {'form': [], 'header': [], 'body': [], 'footer': []}
        self._widgets = {}
        self._validator = Validator()

        if not self._name:
            self._name = uid

        self.add_widget(HiddenInputWidget(name='__form_location', value=router.current_url()), area='form')
        self.add_widget(WrapperWidget(cls='form-messages'))

        self._setup()

        # Initializing form JS API
        assetman.add_js('pytsite.core@js/form.js')

    def _setup(self):
        """_setup() hook.
        """
        pass

    @property
    def uid(self) -> str:
        """Get form ID.
        """
        return self._uid

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

    @property
    def action(self) -> str:
        """Get form action URL.
        """
        return self._action

    @action.setter
    def action(self, val):
        """Set form action URL.
        """
        self._action = val

    @property
    def legend(self) -> str:
        """Get legend.
        """
        return self._legend

    @legend.setter
    def legend(self, value: str):
        """Set legend.
        """
        self._legend = value

    @property
    def cls(self) -> str:
        """Get CSS classes.
        """
        return self._cls

    @cls.setter
    def cls(self, value):
        """Set CSS classes.
        """
        self._cls = 'pytsite-form ' + value

    @property
    def messages(self):
        """Get validation messages.
        """
        return self._validator.messages

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

        r = {}
        for k, v in self._widgets.items():
            r[k] = v['widget'].get_value()

        return r

    def fill(self, values: dict, **kwargs: dict):
        """Fill form's widgets with values.
        """

        for field_name, field_value in values.items():
            if self.has_widget(field_name):
                self.get_widget(field_name).set_value(field_value, **kwargs)

                # Setting value of the validator
                if self._validator.has_field(field_name):
                    self._validator.set_value(field_name, self.get_widget(field_name).get_value())

        return self

    def add_rule(self, widget_uid: str, rule: BaseRule):
        """Add a rule to the validator.
        """

        if widget_uid not in self._widgets:
            raise KeyError("Widget '{0}' is not exists.".format(widget_uid))

        self._validator.add_rule(widget_uid, rule)

        return self

    def add_rules(self, widget_uid: str, rules: tuple):
        """Add multiple rules to the validator.
        """

        for rule in rules:
            self.add_rule(widget_uid, rule)

        return self

    def validate(self) -> bool:
        """Validate the form.
        """
        return self._validator.validate()

    def store_state(self, except_fields: tuple=None):
        """Store state of the form into the session.
        """
        pass

    def restore_state(self, except_fields: tuple=None):
        """Store state of the form from the session.
        """
        pass

    def render(self) -> str:
        """Render the form.
        """

        if self._legend:
            self.add_widget(HtmlWidget(value=self._legend, html_em=H3, cls='box-title'), area='header')

        body = ''
        for area in ['form', 'header', 'body', 'footer']:
            rendered_area = self._render_widgets(area)
            body += rendered_area

        return self._render_open_tag() + body + self._render_close_tag()

    def add_widget(self, widget: AbstractWidget, weight: int=0, area: str='body'):
        """Add a widget.
        """

        uid = widget.uid
        if uid in self._widgets:
            raise KeyError("Widget '{0}' already exists.".format(uid))

        self._widgets[uid] = {'widget': widget, 'weight': weight}
        self._areas[area].append(uid)

        return self

    def has_widget(self, uid: str) -> bool:
        """Check if the form has widget.
        """

        return uid in self._widgets

    def get_widget(self, uid: str) -> AbstractWidget:
        """Get a widget.
        """

        if not self.has_widget(uid):
            raise KeyError("Widget '{0}' is not exists.".format(uid))

        return self._widgets[uid]['widget']

    def _render_open_tag(self) -> str:
        """Render form's open tag.
        """

        attrs = {
            'id': self.uid,
            'name': self.name,
            'class': self.cls,
            'action': self.action,
            'method': self.method,
            'data-validation-ep': self.validation_ep,
        }

        r = '<form {}>\n'.format(xml_attrs_str(attrs))

        return r + '\n'

    def _render_widgets(self, area: str) -> str:
        """Render widgets.
        """

        widgets_to_render = {}
        for widget_uid in self._areas[area]:
            widgets_to_render[widget_uid] = self._widgets[widget_uid]

        rendered_widgets = []
        for k, v in dict_sort(widgets_to_render):
            rendered_widgets.append(v['widget'].render())

        if not rendered_widgets:
            return ''

        return self._render_area(area, '\n'.join(rendered_widgets))

    def _render_area(self, area: str, content: str):
        """Render area.
        """

        if area == 'form':
            return content + '\n'
        else:
            cls = 'box-' + area
            if area == 'header':
                cls += ' with-border'
            return Div(content + '\n', cls=cls).render()

    def _render_close_tag(self) -> str:
        """Render form's close tag.
        """

        return '</form>\n'
