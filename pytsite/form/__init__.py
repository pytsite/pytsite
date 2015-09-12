"""Pytsite Form
"""
from urllib.parse import unquote as _url_unquote
from collections import OrderedDict as _OrderedDict
from pytsite import util as _util, widget as _widget, html as _html, router as _router, assetman as _assetman, \
    validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_assetman.register_package(__name__)


class Base:
    """Abstract form.
    """
    def __init__(self, uid: str, **kwargs: dict):
        """Init.
        """
        self._areas = ('form', 'header', 'body', 'footer')
        self._widgets = _OrderedDict()
        self._validator = _validation.Validator()

        self._uid = uid
        self._name = kwargs.get('name', None)
        self._method = kwargs.get('method', 'post')
        self._action = kwargs.get('action', '#')
        self._legend = kwargs.get('legend', None)
        self._css = kwargs.get('css', 'pytsite-form')
        self._validation_ep = kwargs.get('validation_ep')

        redirect_url = _router.request.values_dict.get('__form_redirect')
        if not redirect_url:
            redirect_url = _router.current_url()
        elif isinstance(redirect_url, list):
            redirect_url = redirect_url[0]

        self.add_widget(_widget.input.Hidden(uid='__form_location', value=_router.current_url()), area='form')
        self.add_widget(_widget.input.Hidden(uid='__form_redirect', value=_url_unquote(redirect_url)), area='form')
        self.add_widget(_widget.static.Wrapper(css='form-messages'))

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
    def css(self) -> str:
        """Get CSS classes.
        """
        return self._css

    @css.setter
    def css(self, value):
        """Set CSS classes.
        """
        self._css = 'pytsite-form ' + value

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
        r = _OrderedDict()
        for k, v in self._widgets.items():
            r[k] = v['_widget'].get_value()

        return r

    @property
    def fields(self) -> list:
        return self._widgets.keys()

    @property
    def redirect(self) -> str:
        """Get after form submit redirect URL.
        """
        return self.get_widget('__form_redirect').get_value()

    @redirect.setter
    def redirect(self, value):
        """Redirect URL after sucessfull form submit.
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
        """Add a rule to the validator.
        """
        if widget_uid not in self._widgets:
            raise KeyError("Widget '{}' is not exists.".format(widget_uid))

        self._validator.add_rule(widget_uid, rule)

        return self

    def add_rules(self, widget_uid: str, rules: tuple):
        """Add multiple rules to the validator.
        """
        for rule in rules:
            self.add_rule(widget_uid, rule)

        return self

    def remove_rules(self, widget_uid: str):
        """Remove validation's rules.
        """
        if widget_uid not in self._widgets:
            raise KeyError("Widget '{}' is not exists.".format(widget_uid))
        self._validator.remove_rules(widget_uid)

    def validate(self) -> bool:
        """Validate the form.
        """
        # Setting values of the validator
        for uid in self.fields:
            if self._validator.has_field(uid):
                self._validator.set_value(uid, self.get_widget(uid).get_value(validation_mode=True))

        return self._validator.validate()

    def render(self) -> str:
        """Render the form.
        """
        if self._legend and not self.has_widget('__form_legend'):
            self.add_widget(
                _widget.static.Html(uid='__form_legend', value=self._legend, html_em=_html.H3, css='box-title'),
                area='header'
            )

        body = ''
        for area in self._areas:
            rendered_area = self._render_widgets(area)
            body += rendered_area

        return self._render_open_tag() + body + self._render_close_tag()

    def __str__(self) -> str:
        """Render the form.
        """
        return self.render()

    def add_widget(self, w: _widget.Base, area: str='body'):
        """Add a widget.
        """
        if area not in self._areas:
            raise ValueError("Invalid form area: '{}'".format(area))

        uid = w.uid
        if uid in self._widgets:
            raise KeyError("Widget '{}' already exists.".format(uid))

        self._widgets[uid] = {'_widget': w, 'area': area}

        return self

    def replace_widget(self, uid: str, replacement: _widget.Base):
        """Replace a widget with another one.
        """
        current = self.get_widget(uid)
        if not replacement.weight and current.weight:
            replacement.weight = current.weight

        replacement.uid = uid

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

        return self._widgets[uid]['_widget']

    def remove_widget(self, uid):
        """Remove widget from the form.
        """
        if uid in self._widgets:
            del self._widgets[uid]

        self._validator.remove_rules(uid)

        return self

    def _render_open_tag(self) -> str:
        """Render form's open tag.
        """
        attrs = {
            'id': self.uid,
            'name': self.name,
            'class': self.css,
            'action': self.action,
            'method': self.method,
            'data-validation-ep': self.validation_ep,
        }

        r = '<form {}>\n'.format(_util.html_attrs_str(attrs))

        return r + '\n'

    def _render_widgets(self, area: str) -> str:
        """Render widgets.
        """
        widgets_to_render = []
        for uid, w in self._widgets.items():
            if w['area'] == area:
                _widget = w['_widget']
                widgets_to_render.append({'weight': _widget.weight, '_widget': _widget})

        rendered_widgets = []
        for v in _util.weight_sort(widgets_to_render):
            rendered_widgets.append(str(v['_widget'].render()))

        if not rendered_widgets:
            return ''

        return self._render_area(area, '\n'.join(rendered_widgets))

    @staticmethod
    def _render_area(area: str, content: str):
        """Render area.
        """
        if area == 'form':
            return content + '\n'
        else:
            cls = 'box-' + area
            if area == 'header':
                cls += ' with-border'
            return _html.Div(content + '\n', cls=cls).render()

    @staticmethod
    def _render_close_tag() -> str:
        """Render form's close tag.
        """
        return '</form>\n'
