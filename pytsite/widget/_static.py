"""Static Widgets.
"""
import re as _re
from pytsite import html as _html
from . import _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class HTML(_base.Abstract):
    """Wrapper widget for pytsite.html.Element instances.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        :param em: pytsite.html.Element
        """
        super().__init__(uid, **kwargs)

        self._em = kwargs.get('em')
        if not self._em:
            raise ValueError('Element is not specified.')

    def get_html_em(self, **kwargs) -> _html.Element:
        return self._em


class Text(_base.Abstract):
    """Static Text Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._css = ' '.join((self._css, 'widget-static-control'))

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        container = _html.TagLessElement()
        container.append(_html.Input(type='hidden', uid=self.uid, name=self.name, value=self.value))
        container.append(_html.P(self.title, cls='form-control-static'))

        return self._group_wrap(container)


class VideoPlayer(_base.Abstract):
    """Video player widget.
    """

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return self._get_embed(self.get_val())

    def _get_embed(self, url: str) -> _html.Element:
        """Get player embed code.
        """
        if url.find('youtube.com') > 0 or url.find('youtu.be') > 0:
            return self._get_embed_youtube(url)
        elif url.find('vimeo.com') > 0:
            return self._get_embed_vimeo(url)
        elif url.find('rutube.ru') > 0:
            return self._get_embed_rutube(url)
        else:
            return _html.Div('Not implemented.')

    @staticmethod
    def _get_embed_youtube(url, width: int = 640, height: int = 480) -> _html.Element:
        """Get YouTube player embed code.
        """
        match = _re.search('(youtube\.com/watch.+v=|youtu.be/)(.{11})', url)
        if match:
            src = '//www.youtube.com/embed/{}?html5=1'.format(match.group(2))
            return _html.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                cls='iframe-responsive')

        raise ValueError(_html.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_vimeo(url, width: int = 640, height: int = 480) -> _html.Element:
        """Get Vimeo player embed code.
        """
        match = _re.search('vimeo\.com/(\d+)', url)
        if match:
            src = '//player.vimeo.com/video/{}'.format(match.group(1))
            return _html.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                cls='iframe-responsive')

        raise ValueError(_html.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_rutube(url, width: int = 640, height: int = 480) -> _html.Element:
        """Get RuTube player embed code.
        """
        match = _re.search('rutube\.ru/video/(\w{32})', url)
        if match:
            src = '//rutube.ru/video/embed/{}'.format(match.group(1))
            return _html.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                cls='iframe-responsive')

        raise ValueError(_html.Div('Invalid video link: ' + url))
