"""Tag Widgets.
"""
from pytsite import widget as _widget, html as _html, odm as _odm, router as _router, tpl as _tpl, odm_ui as _odm_ui, \
    lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TermSelect(_odm_ui.widget.EntitySelect):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)
        self._language = kwargs.get('language', _lang.get_current())

    def _get_finder(self):
        finder = super()._get_finder()
        finder.eq('language', self._language)

        return finder


class TokensInput(_widget.input.Tokens):
    """Term Tokens Input Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = []

        super().__init__(uid, **kwargs)

        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._remote_source = _router.ep_url('pytsite.taxonomy@search_terms', {
            'model': self._model,
            'query': '__QUERY'
        })

        self._data.update({
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        })

        self._assets.append('pytsite.taxonomy@js/widget/tokens-input.js')

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if value is None:
            return super().set_val(value, **kwargs)

        if isinstance(value, str):
            value = value.split(',')

        clean_value = []
        for v in value:
            if isinstance(v, _odm.model.Entity):
                clean_value.append(v)
            elif isinstance(v, str) and v:
                term = _api.dispense(self._model, v)
                with term:
                    clean_value.append(term.save())

        super().set_val(clean_value)

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        html_input = _html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=','.join([v.f_get('title') for v in self.get_val()]),
            cls=' '.join(('form-control', self._css)),
        )

        return self._group_wrap(html_input)


class Cloud(_widget.Abstract):
    """Tags Cloud Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')
        if not _api.is_model_registered(self._model):
            raise ValueError("'{}' is not a registered taxonomy model.".format(self._model))

        self._tpl = kwargs.get('tpl', 'pytsite.taxonomy@widget/cloud')
        self._num = kwargs.get('num', 10)
        self._link_pattern = kwargs.get('link_pattern', '/{}/%s'.format(self._model))
        self._term_title_pattern = kwargs.get('term_title_pattern', '%s')
        self._term_css = kwargs.get('term_css', 'label label-default')
        self._title_tag = kwargs.get('title_tag', 'h3')
        self._wrap = kwargs.get('wrap', True)

        self._css += ' widget-taxonomy-cloud widget-taxonomy-cloud-{}'.format(self._model)

        self._assets.append('pytsite.taxonomy@css/taxonomy.css')

    @property
    def model(self) -> str:
        return self._model

    @property
    def num(self) -> int:
        return self._num

    @property
    def link_pattern(self) -> str:
        return self._link_pattern

    @property
    def term_title_pattern(self) -> str:
        return self._term_title_pattern

    @property
    def term_css(self) -> str:
        return self._term_css

    @property
    def title_tag(self) -> str:
        return self._title_tag

    @property
    def terms(self) -> list:
        return list(_api.find(self._model).get(self._num))

    @property
    def wrap(self) -> bool:
        return self._wrap

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        content = _html.TagLessElement(_tpl.render(self._tpl, {'widget': self}))
        if self._wrap:
            content = self._group_wrap(content)

        return content
