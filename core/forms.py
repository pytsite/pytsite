__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from abc import ABC, abstractmethod
from .widget import AbstractWidget
from .validation import Validator, Rule


class AbstractForm(ABC):
    def __init__(self, uid: str, name: str=None, legend: str=None, css_classes: tuple=()):
        """Init.
        """
        self._id = uid
        self._name = name if name else uid
        self._legend = legend
        self._css_classes = css_classes
        self._widgets = {}
        self._validator = Validator()

        self._setup()

    @abstractmethod
    def _setup(self):
        """_setup() hook.
        """
        pass

    def fill(self, values: dict):
        """Fill form's widgets with values.
        """
        if not isinstance(values, dict):
            raise TypeError('Dict expected.')

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

    def validate(self):
        """Validate the form.
        """
        return self._validator.validate()

    @property
    def messages(self):
        """Get validation messages.
        """
        return self._validator.messages

    def render(self)->str:
        """Render the form.
        """
        header = self._render_header()
        footer = self._render_footer()
        body = []
        for widget_data in sorted(self._widgets.items(), key=lambda item: item[1][1]):
            body.append(widget_data[1][0].render())

        return header + '\n'.join(body) + '\n' + footer

    def _add_widget(self, widget: AbstractWidget, weight: int=0):
        """Add a widget.
        """
        uid = widget.uid
        if uid in self._widgets:
            raise KeyError("Widget '{0}' already exists.".format(uid))

        self._widgets[uid] = (widget, weight)

        return self

    def _has_widget(self, uid: str)->bool:
        return uid in self._widgets

    def _get_widget(self, uid: str)->AbstractWidget:
        """Get a widget.
        """
        if not self._has_widget(uid):
            raise KeyError("Widget '{0}' is not exists.".format(uid))

        return self._widgets[uid][0]

    def _render_header(self):
        """Render the header of the form.
        """
        css_class = ''
        if self._css_classes:
            css_class = 'class="{0}"'.format(' '.join(self._css_classes))

        r = '<form {0} id="{1}" name="{2}">\n'.format(css_class, self._id, self._name)

        return r

    def _render_footer(self)->str:
        """Render form's footer.
        """
        return '</form>\n'
