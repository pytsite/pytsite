"""AddThis Widget.
"""
from pytsite import reg as _reg, assetman as _assetman, html as _html
from pytsite import widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AddThis(_widget.Base):
    """AddThis Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._pub_id = _reg.get('addthis.pub_id')
        if not self._pub_id:
            raise Exception("Configuration parameter 'addthis.pub_id' is not defined.")

        self._valid_types = ('sharing_toolbox', 'recommended_horizontal')
        self._box_type = kwargs.get('box_type', 'sharing_toolbox')
        if self._box_type not in self._valid_types:
            raise Exception("Invalid type: '{}'. Valid types are: {}.".format(self._box_type, str(self._valid_types)))

        self._url = kwargs.get('url')

        _assetman.add('//s7.addthis.com/js/300/addthis_widget.js#pubid=' + self._pub_id)

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        div = _html.Div(cls='addthis_' + self._box_type)

        if self._url:
            div.set_attr('data_url', self._url)
        if self._title:
            div.set_attr('data_title', self._title)

        return div
