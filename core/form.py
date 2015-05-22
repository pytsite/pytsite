"""Forms.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from .widget.abstract import AbstractWidget
from .validation import Validator, Rule
from .html import Div


class AbstractForm(ABC):
    """Abstract form.
    """
    def __init__(self, uid: str, **kwargs: dict):
        """Init.
        """
        self._uid = uid
        self._name = kwargs.get('name', '')
        self._action = kwargs.get('action', '')
        self._legend = kwargs.get('legend', '')
        self._classes = kwargs.get('classes', '')

        self._areas = {'header': [], 'body': [], 'footer': []}
        self._widgets = {}
        self._validator = Validator()

        if not self._name:
            self._name = uid

        self._setup()

    @abstractmethod
    def _setup(self):
        """_setup() hook.
        """
        raise NotImplementedError()

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @property
    def action(self) -> str:
        return self._action

    @action.setter
    def action(self, val):
        self._action = val

    @property
    def legend(self) -> str:
        return self._legend

    @property
    def classes(self) -> str:
        return self._classes

    def fill(self, values: dict):
        """Fill form's widgets with values.
        """

        for field_name, field_value in values.items():
            if self._has_widget(field_name):
                self._get_widget(field_name).value = field_value

            if self._validator.has_field(field_name):
                self._validator.set_value(field_name, field_value)

        return self

    def add_rule(self, widget_id: str, rule: Rule):
        """Add a rule to the validator.
        """

        if widget_id not in self._widgets:
            raise KeyError("Widget '{0}' is not exists.".format(widget_id))

        self._validator.add_rule(widget_id, rule)

        return self

    def validate(self) -> bool:
        """Validate the form.
        """

        return self._validator.validate()

    @property
    def messages(self):
        """Get validation messages.
        """
        return self._validator.messages

    def render(self) -> str:
        """Render the form.
        """

        body = ''
        for area in ['header', 'body', 'footer']:
            rendered_area = self._render_widgets(area)
            body += rendered_area

        return self._render_header() + body + self._render_footer()

    def add_widget(self, widget: AbstractWidget, weight: int=0, area: str='body'):
        """Add a widget.
        """

        uid = widget.uid
        if uid in self._widgets:
            raise KeyError("Widget '{0}' already exists.".format(uid))

        self._widgets[uid] = (widget, weight)
        self._areas[area].append(uid)

        return self

    def _has_widget(self, uid: str) -> bool:

        return uid in self._widgets

    def _get_widget(self, uid: str) -> AbstractWidget:
        """Get a widget.
        """

        if not self._has_widget(uid):
            raise KeyError("Widget '{0}' is not exists.".format(uid))

        return self._widgets[uid][0]

    def _render_header(self) -> str:
        """Render the header of the form.
        """

        css_class = ''
        if self._classes:
            css_class = 'class="{}"'.format(' '.join(self._classes))

        r = '<form action="{}" {} id="{}" name="{}">\n'.format(self.action, css_class, self._uid, self._name)

        return r + '\n'

    def _render_widgets(self, area: str) -> str:

        widgets_to_render = {}
        for widget_uid in self._areas[area]:
            widgets_to_render[widget_uid] = self._widgets[widget_uid]

        rendered_widgets = []
        for widget_data in sorted(widgets_to_render.items(), key=lambda item: item[1][1]):
            rendered_widgets.append(widget_data[1][0].render())

        if not rendered_widgets:
            return ''

        return Div('\n'.join(rendered_widgets) + '\n', cls='box-' + area).render()

    def _render_footer(self) -> str:
        """Render form's footer.
        """

        return '</form>\n'
