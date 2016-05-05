"""Static Widgets.
"""
import re as _re
from math import ceil as _ceil

from pytsite import html as _html, lang as _lang, router as _router
from . import _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class HTML(_base.Base):
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


class Text(_base.Base):
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


class Tabs(_base.Base):
    """Tabs Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._tabs = []

    def add_tab(self, tid: str, title: str, content: str):
        """Add a tab.
        """
        tid = tid.replace('.', '-')
        self._tabs.append((tid, title, content))
        return self

    def get_html_em(self, **kwargs) -> str:
        wrapper = _html.Div(role='tabpanel')
        tabs_ul = _html.Ul(cls='nav nav-tabs', role='tablist')
        content = _html.Div(cls='tab-content')
        wrapper.append(tabs_ul).append(content)

        i = 0
        for tab in self._tabs:
            tab_uid = 'tab-uid-' + tab[0]
            tabs_ul.append(
                _html.Li(role='presentation', cls='active' if i == 0 else '').append(
                    _html.A(tab[1], href='#' + tab_uid, role='tab', data_toggle='tab')
                )
            )
            content_cls = 'tabpanel tab-pane'
            content_cls += ' active' if i == 0 else ''
            content.append(_html.Div(tab[2], cls=content_cls, uid=tab_uid))
            i += 1

        return self._group_wrap(wrapper)


class VideoPlayer(_base.Base):
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


class Pager(_base.Base):
    """Pager Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        inp = _router.request().inp

        self._total_items = int(kwargs.get('total_items'))
        self._items_per_page = int(kwargs.get('per_page', 100))
        self._total_pages = _ceil(self._total_items / self._items_per_page)
        self._visible_numbers = int(kwargs.get('visible_numbers', 5)) - 1
        self._current_page = inp['page'] if ('page' in inp and isinstance(inp['page'], int)) else 1

        if self._current_page < 1:
            self._current_page = 1
        if self._current_page > self._total_pages:
            self._current_page = self._total_pages

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        if self._total_pages == 1:
            return _html.TagLessElement()

        start_visible_num = self._current_page - _ceil(self._visible_numbers / 2)
        if start_visible_num < 1:
            start_visible_num = 1
        end_visible_num = start_visible_num + self._visible_numbers

        if end_visible_num > self._total_pages:
            end_visible_num = self._total_pages

        ul = _html.Ul(cls='pagination')
        if start_visible_num > 1:
            li = _html.Li(cls='first-page')
            a = _html.A('«', title=_lang.t('pytsite.widget@first_page'),
                        href=_router.url(_router.current_url(), query={'page': 1}))
            ul.append(li.append(a))

            li = _html.Li(cls='previous-page')
            a = _html.A('‹', title=_lang.t('pytsite.widget@previous_page'),
                        href=_router.url(_router.current_url(), query={'page': self._current_page - 1}))
            ul.append(li.append(a))

        for num in range(start_visible_num, end_visible_num + 1):
            li = _html.Li()
            if self._current_page == num:
                li.set_attr('cls', 'active')
            a = _html.A(str(num), href=_router.url(_router.current_url(), query={'page': num}))
            ul.append(li.append(a))

        if end_visible_num < self.total_pages:
            li = _html.Li(cls='next-page')
            a = _html.A('›', title=_lang.t('pytsite.widget@next_page'),
                        href=_router.url(_router.current_url(), query={'page': self._current_page + 1}))
            ul.append(li.append(a))

            li = _html.Li(cls='last-page')
            a = _html.A('»', title=_lang.t('pytsite.widget@last_page'),
                        href=_router.url(_router.current_url(), query={'page': self.total_pages}))
            ul.append(li.append(a))

        return ul

    @property
    def skip(self):
        skip = (self._current_page - 1) * self._items_per_page
        return skip if skip >= 0 else 0

    @property
    def limit(self):
        return self._items_per_page

    @property
    def total_items(self):
        return self._total_items

    @property
    def total_pages(self):
        return self._total_pages
