"""Tag Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router
from pytsite.core.widgets.selectable import TokenSelectWidget
from pytsite.core.html import Input
from pytsite.core.odm.models import ODMModel
from . import taxonomy_manager


class TermTokenInputWidget(TokenSelectWidget):

    def __init__(self, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')

        super().__init__(**kwargs)

        if not self._model:
            raise Exception('Model is required.')

        self._remote_source = router.endpoint_url('pytsite.taxonomy.eps.search_terms', {
            'model': self._model,
            'query': '__QUERY'
        })

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            return super().set_value([])

        if isinstance(value, str):
            value = value.split(',')

        clean_value = []
        for v in value:
            if isinstance(v, ODMModel):
                clean_value.append(v)
            elif isinstance(v, str):
                clean_value.append(taxonomy_manager.dispense(self._model, v).save())

        super().set_value(clean_value)

    def render(self) -> str:
        """Render the widget.
        """
        html_input = Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=','.join([v.f_get('title') for v in self.get_value()]),
            cls=' '.join(('form-control', self._cls)),
        )

        return self._group_wrap(html_input, {
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        })
