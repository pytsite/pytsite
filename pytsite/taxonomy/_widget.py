"""Tag Widgets.
"""
from pytsite import widget as _widget, html as _html, odm as _odm, router as _router, tpl as _tpl
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TokensInput(_widget.input.Tokens):
    """Term Tokens Input Widget.
    """
    def __init__(self, model: str, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        self._model = model
        self._remote_source = _router.ep_url('pytsite.taxonomy.eps.search_terms', {
            'model': self._model,
            'query': '__QUERY'
        })

        self._data = {
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
            cls=' '.join(('form-control', self._css)),
        )

        return self._group_wrap(html_input)


class Cloud(_widget.Base):
    """Tags Cloud Widget.
    """
    def __init__(self, model: str, tpl='pytsite.taxonomy@widget/cloud', **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        self._model = model
        if not _functions.is_model_registered(model):
            raise ValueError("'{}' is not a registered taxonomy model.".format(model))

        self._tpl = tpl
        self._num = kwargs.get('num', 10)
        self._link_pattern = kwargs.get('link_pattern', '/{}/%s'.format(model))
        self._term_title_pattern = kwargs.get('term_title_pattern', '%s')
        self._term_css = kwargs.get('term_css', 'label label-default')
        self._title_tag = kwargs.get('title_tag', 'h3')
        self._wrap = kwargs.get('wrap', True)

        self._css += ' widget-taxonomy-cloud widget-taxonomy-cloud-{}'.format(self._model)

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
        return list(_functions.find(self._model).get(self._num))

    @property
    def wrap(self) -> bool:
        return self._wrap

    def render(self) -> _html.Element:
        """Render the widget.
        """
        content = _html.TagLessElement(_tpl.render(self._tpl, {'widget': self}))
        if self._wrap:
            content = self._group_wrap(content)

        return content
