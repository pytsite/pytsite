"""Tag Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router as _router, widget as _widget, html as _html, odm as _odm
from . import _manager


class TermTokens(_widget.select.Tokens):

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
            if isinstance(v, _odm.model.ODMModel):
                clean_value.append(v)
            elif isinstance(v, str):
                clean_value.append(_manager.dispense(self._model, v).save())

        super().set_value(clean_value)

    def render(self) -> str:
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
