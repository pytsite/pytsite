"""Tag Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router as _router, widget as _widget, html as _html, odm as _odm
from . import _functions


class TokensInput(_widget.select.Tokens):
    """Term Tokens Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')

        super().__init__(**kwargs)

        if not self._model:
            raise Exception('Model is required.')

        self._remote_source = _router.endpoint_url('pytsite.taxonomy.eps.search_terms', {
            'model': self._model,
            'query': '__QUERY'
        })

        self._group_data = {
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        }

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            return super().set_value([])

        if isinstance(value, str):
            value = value.split(',')

        clean_value = []
        for v in value:
            if isinstance(v, _odm.Model):
                clean_value.append(v)
            elif isinstance(v, str):
                clean_value.append(_functions.dispense(self._model, v).save())

        super().set_value(clean_value)

    def render(self) -> _html.Element:
        """Render the widget.
        """
        html_input = _html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=','.join([v.f_get('title') for v in self.get_value()]),
            cls=' '.join(('form-control', self._cls)),
        )

        return self._group_wrap(html_input)

class Cloud(_widget.Base):
    """Tags Cloud Widget.
    """
    def __init__(self, model: str, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        self._model = model
        if not _functions.is_model_registered(model):
            raise ValueError("'{}' is not a registered taxonomy model.".format(model))

        self._num = kwargs.get('num', 10)
        self._link_pattern = kwargs.get('link_pattern', '/{}/%s'.format(model))
        self._title_pattern = kwargs.get('title_pattern', '#%s')
        self._term_css = kwargs.get('term_css', 'label label-default')

        self._group_cls += ' widget-taxonomy-cloud'

    def render(self) -> _html.Element:
        """Render the widget.
        """
        root = _html.Div(child_separator='  ')
        weight = 10
        for term in self._get_finder().get(self._num):
            title = self._title_pattern % term.f_get('title')
            a_cls = 'term {} weight-{} {}'.format(self._model, weight, self._term_css)
            a = _html.A(title, href=self._link_pattern % term.f_get('alias'), cls=a_cls)
            root.append(a)
            weight -= 1

        return self._group_wrap(root)

    def _get_finder(self):
        _functions.find(self._model)