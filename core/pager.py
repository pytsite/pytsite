"""Pager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from math import ceil, floor
from pytsite.core.router import request, url, current_url
from pytsite.core.html import Ul, Li, A


class Pager:
    def __init__(self, total_items: int, per_page: int=100, visible_pages: int=10):
        self._total_items = total_items
        self._items_per_page = per_page
        self._total_pages = ceil(total_items / per_page)
        self._visible_pages = visible_pages
        self._current_page = request.values.get('page', 1)

        if self._current_page > self._total_pages:
            self._current_page = self._total_pages

    def render(self):
        start_visible_page = self._current_page - self._visible_pages
        end_visible_page = start_visible_page + self._visible_pages

        if end_visible_page > self._total_pages:
            end_visible_page = self._total_pages
            start_visible_page = end_visible_page - self._visible_pages

        ul = Ul(class_='pagination')
        for page_num in range(start_visible_page, end_visible_page):
            href = url(current_url(), query={'page': page_num})

            li = Li()
            if self._current_page == page_num:
                li.set_attr('class', 'active')

            li.append(A(str(page_num), href=href))
            ul.append(li)

        return ul.render()

    @property
    def offset(self):
        return self._current_page * self._items_per_page

    @property
    def per_page(self):
        return self.per_page
