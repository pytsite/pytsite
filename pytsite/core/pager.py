"""Pager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from math import ceil as _ceil
from . import router as _router, html as _html


class Pager:
    def __init__(self, total_items: int, per_page: int=100, visible_pages: int=10):
        self._total_items = total_items
        self._items_per_page = per_page
        self._total_pages = _ceil(total_items / per_page)
        self._visible_pages = visible_pages
        self._current_page = _router.request.values.get('page', 1)

        if self._current_page > self._total_pages:
            self._current_page = self._total_pages

    def render(self):
        start_visible_page = self._current_page - self._visible_pages
        end_visible_page = start_visible_page + self._visible_pages

        if end_visible_page > self._total_pages:
            end_visible_page = self._total_pages
            start_visible_page = end_visible_page - self._visible_pages

        ul = _html.Ul(cls='pagination')
        for page_num in range(start_visible_page, end_visible_page):
            href = _router.url(_router.current_url(), query={'page': page_num})

            li = _html.Li()
            if self._current_page == page_num:
                li.set_attr('class', 'active')

            li.append(_html.A(str(page_num), href=href))
            ul.append(li)

        return ul.render()

    @property
    def skip(self):
        if self._current_page == 1:
            return 0
        return self._current_page * self._items_per_page

    @property
    def limit(self):
        return self._items_per_page

    @property
    def total_items(self):
        return self._total_items

    @property
    def total_pages(self):
        return self._total_pages
