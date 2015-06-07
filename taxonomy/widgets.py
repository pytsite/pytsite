"""Tag Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router
from pytsite.core.widgets.selectable import TokenSelectWidget


class TermTokenInputWidget(TokenSelectWidget):

    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._model = kwargs.get('model')
        if not self._model:
            raise Exception('Model is required.')

        self._remote_source = router.endpoint_url('pytsite.taxonomy.eps.search_terms', {
            'model': self._model,
            'query': '__QUERY'
        })
