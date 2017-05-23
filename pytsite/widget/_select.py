"""PytSite Select Widgets.
"""
from typing import Union as _Union, List as _List, Tuple as _Tuple
from collections import OrderedDict as _OrderedDict
from math import ceil as _ceil
from datetime import datetime as _datetime
from pytsite import html as _html, lang as _lang, validation as _validation, util as _util, hreflang as _hreflang, \
    router as _router
from . import _input, _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Checkbox(_input.Input):
    """Single Checkbox Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        kwargs.setdefault('label_disabled', True)
        super().__init__(uid, **kwargs)

    def set_val(self, value, **kwargs):
        # If checkbox is checked on client side, we get list of 2 two items: ['', 'True'],
        # or empty string otherwise
        if isinstance(value, list):
            value = value[-1] if value else False

        super().set_val(True if value in (True, 'True') else False, **kwargs)

    @property
    def checked(self) -> bool:
        return self.get_val()

    @checked.setter
    def checked(self, value: bool):
        self.set_val(value)

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        """
        div = _html.Div(css='checkbox')
        div.append(_html.Input(type='hidden', name=self._name))
        label = _html.Label(self._label, label_for=self._uid)
        label.append(_html.Input(
            uid=self._uid, name=self._name, type='checkbox', value='True', checked=self.checked
        ))
        div.append(label)

        return div


class Select(_input.Input):
    """Select Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._items = kwargs.get('items', [])
        if type(self._items) not in (list, tuple):
            raise TypeError('List or tuple expected.')

        self._append_none_item = kwargs.get('append_none_item', True)

    def _get_select_html_em(self) -> _html.Element:
        select = _html.Select(name=self.name, css='form-control', required=self._required)

        if self._append_none_item:
            select.append(_html.Option('--- ' + _lang.t('pytsite.widget@select_none_item') + ' ---', value=''))

        for item in self._items:
            option = _html.Option(item[1], value=item[0])
            if item[0] == self._value:
                option.set_attr('selected', True)
            select.append(option)

        return select

    def _get_element(self, **kwargs):
        """Render the widget.
        :param **kwargs:
        """
        return self._get_select_html_em()


class Select2(Select):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._js_module = 'pytsite-widget-select-select2'
        self._theme = kwargs.get('theme', 'bootstrap')
        self._ajax_url = kwargs.get('ajax_url')
        self._ajax_delay = kwargs.get('ajax_delay', 750)
        self._ajax_data_type = kwargs.get('ajax_data_type', 'json')
        self._css += ' widget-select-select2'

    def _get_element(self, **kwargs) -> _html.Element:
        select = self._get_select_html_em()
        select.set_attr('style', 'width: 100%;')

        if self._ajax_url:
            select.set_attr('data_theme', self._theme)
            select.set_attr('data_ajax_url', self._ajax_url)
            select.set_attr('data_ajax_delay', self._ajax_delay)
            select.set_attr('data_ajax_data_type', self._ajax_data_type)

        return select


class Checkboxes(Select):
    """Group of Checkboxes Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        kwargs.setdefault('default', ())

        self._unique = kwargs.get('unique', False)

        super().__init__(uid, **kwargs)

    def set_val(self, value: _Union[_List, _Tuple], **kwargs):
        """Set value of the widget.
        """
        super().set_val(_util.cleanup_list(value, self._unique))

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        container = _html.TagLessElement()
        container.append(_html.Input(type='hidden', name=self.name + '[]'))
        for item in self._items:
            checked = True if item[0] in self.value else False
            container.append(
                _html.Div(css='checkbox').append(
                    _html.Label(item[1]).append(
                        _html.Input(type='checkbox', name=self.name + '[]', value=item[0], checked=checked)
                    )
                )
            )

        return container


class Language(Select):
    """Select Language Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._items = kwargs.get('items', [])

        for code in _lang.langs():
            self._items.append((code, _lang.lang_title(code)))


class LanguageNav(_base.Abstract):
    """Language Nav Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._wrap_em = _html.Ul()
        self._group_wrap = False
        self._dropdown = kwargs.get('dropdown')
        self._dropup = kwargs.get('dropup')
        self._css += ' nav navbar-nav widget-select-language-nav'
        self._language_titles = kwargs.get('language_titles', {})

    def _get_element(self, **kwargs) -> _html.Element:
        if len(_lang.langs()) == 1:
            return _html.TagLessElement()

        root = _html.TagLessElement()

        # Dropdown menu
        if self._dropdown or self._dropup:
            # Root element
            dropdown_root = _html.Li(css='dropdown' if self._dropdown else 'dropup')
            toggle_a = _html.A(
                self._language_titles.get(self._language) or _lang.lang_title(self.language),
                css='dropdown-toggle lang-' + self.language,
                data_toggle='dropdown',
                role='button',
                aria_haspopup='true',
                aria_expanded='false',
                href='#',
                content_first=True)
            toggle_a.append(_html.Span(css='caret'))

            # Children
            dropdown_menu = _html.Ul(css='dropdown-menu')
            for lng in _lang.langs():
                if lng != self._language:
                    hl = _hreflang.get(lng)
                    lng_title = self._language_titles.get(lng) or _lang.lang_title(lng)
                    if hl:
                        dropdown_menu.append(
                            _html.Li().append(_html.A(lng_title, css='lang-' + lng, href=hl)))
                    else:
                        # Link to homepage
                        dropdown_menu.append(_html.Li().append(
                            _html.A(lng_title, css='lang-' + lng, href=_router.base_url(lang=lng))))

            dropdown_root.append(toggle_a).append(dropdown_menu)
            root.append(dropdown_root)
        else:
            # Simple list
            for lng in _lang.langs(True):
                lng_title = self._language_titles.get(lng) or _lang.lang_title(lng)
                if lng == self._language:
                    # Active language
                    root.append(_html.Li(css='active').append(
                        _html.A(lng_title, css='lang-' + lng, href=_router.current_url(), title=lng_title)))
                elif _hreflang.get(lng):
                    # Inactive language, related link
                    root.append(_html.Li().append(
                        _html.A(lng_title, css='lang-' + lng, href=_hreflang.get(lng), title=lng_title)))
                else:
                    # Link to homepage, no related link found
                    root.append(_html.Li().append(
                        _html.A(lng_title, css='lang-' + lng, href=_router.base_url(lang=lng), title=lng_title)))

        return root


class DateTime(_input.Text):
    """Date/Time Select Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        kwargs['default'] = kwargs.get('default', _datetime.now())

        super().__init__(uid, **kwargs)

        self._js_module = 'pytsite-widget-select-date-time'
        self._css = self._css.replace('widget-input-text', 'widget-select-datetime')
        self.add_rule(_validation.rule.DateTime())

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, str):
            value = value.strip()
            if value:
                value = _datetime.strptime(value, '%d.%m.%Y %H:%M')
            else:
                value = _datetime.now()

        return super().set_val(value, **kwargs)

    def get_val(self, **kwargs) -> _datetime:
        """Get value of the widget.
        """
        return super().get_val(**kwargs)

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget
        :param **kwargs:
        """
        html_input = _html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self.get_val().strftime('%d.%m.%Y %H:%M'),
            css=' '.join(('form-control', self._css)),
            required=self._required,
        )

        return html_input


class Pager(_base.Abstract):
    """Pager Widget.
    """

    def __init__(self, uid: str, total_items: int, per_page: int = 100, visible_numbers: int = 5,
                 http_api_ep: str = None, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._group_wrap = False

        self._total_items = total_items
        self._items_per_page = per_page
        self._http_api_ep = http_api_ep
        self._total_pages = int(_ceil(self._total_items / self._items_per_page))
        self._visible_numbers = visible_numbers

        if self._visible_numbers > self._total_pages:
            self._visible_numbers = self._total_pages

        # Detect current page
        try:
            self._current_page = int(_router.request().inp.get('page', 1))
        except ValueError:
            self._current_page = 1

        if self._current_page > self._total_pages:
            self._current_page = self._total_pages
        if self._current_page < 1:
            self._current_page = 1

        self._data['http_api_ep'] = self._http_api_ep
        self._data['total_items'] = self._total_items
        self._data['current_page'] = self._current_page
        self._data['total_pages'] = self._total_pages
        self._data['per_page'] = self._items_per_page
        self._data['visible_numbers'] = self._visible_numbers

        self._js_module = 'pytsite-widget-select-pager'

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        if self._total_pages == 0:
            return _html.TagLessElement()

        if self._total_pages == 1:
            self._hidden = True

        start_visible_num = self._current_page - _ceil((self._visible_numbers - 1) / 2)
        if start_visible_num < 1:
            start_visible_num = 1
        end_visible_num = start_visible_num + (self._visible_numbers - 1)

        if end_visible_num > self._total_pages:
            end_visible_num = self._total_pages
            start_visible_num = end_visible_num - (self._visible_numbers - 1)

        ul = _html.Ul(css='pagination')
        links_url = _router.current_url()

        # Link to the first page
        li = _html.Li(css='first-page')
        a = _html.A('«', title=_lang.t('pytsite.widget@first_page'), href=_router.url(links_url, query={'page': 1}))
        ul.append(li.append(a))

        # Link to the previous page
        li = _html.Li(css='previous-page')
        a = _html.A('‹', title=_lang.t('pytsite.widget@previous_page'),
                    href=_router.url(links_url, query={'page': self._current_page - 1}))
        ul.append(li.append(a))

        # Links to visible pages
        for num in range(start_visible_num, end_visible_num + 1):
            li = _html.Li(css='page', data_page=num)
            if self._current_page == num:
                li.set_attr('css', 'page active')
            a = _html.A(str(num), title=_lang.t('pytsite.widget@page_num', {'num': num}),
                        href=_router.url(links_url, query={'page': num}))
            ul.append(li.append(a))

        # Link to the next page
        li = _html.Li(css='next-page')
        a = _html.A('›', title=_lang.t('pytsite.widget@next_page'),
                    href=_router.url(links_url, query={'page': self._current_page + 1}))
        ul.append(li.append(a))

        # Link to the last page
        li = _html.Li(css='last-page')
        a = _html.A('»', title=_lang.t('pytsite.widget@page_num', {'num': self._total_pages}),
                    href=_router.url(links_url, query={'page': self._total_pages}))
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


class Tabs(_base.Abstract):
    """Tabs Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._tabs = _OrderedDict()

    def add_tab(self, tab_id: str, title: str):
        """Add a tab.
        """
        tab_id = tab_id.replace('.', '-')
        if tab_id in self._tabs:
            raise RuntimeError("Tab '{}' is already added".format(tab_id))

        self._tabs[tab_id] = {'title': title, 'widgets': []}

        return self

    def append_child(self, widget: _base.Abstract, tab_id: str = None) -> _base.Abstract:
        """Add a child widget.
        """
        if not self._tabs:
            raise RuntimeError('At least one tab should exists before you can add widgets')

        if not tab_id:
            tab_id = list(self._tabs.keys())[0]

        super().append_child(widget)

        self._tabs[tab_id]['widgets'].append(widget)

        return widget

    def _get_element(self, **kwargs) -> _html.Element:
        tab_panel = _html.Div(role='tabpanel')
        tabs_nav = _html.Ul(css='nav nav-tabs', role='tablist')
        tabs_content = _html.Div(css='tab-content')
        tab_panel.append(tabs_nav).append(tabs_content)

        tab_count = 0
        for tab_id, tab in self._tabs.items():
            tabs_nav.append(
                _html.Li(role='presentation', css='active' if tab_count == 0 else '').append(
                    _html.A(tab['title'], href='#tab-uid-' + tab_id, role='tab', data_toggle='tab')
                )
            )
            tab_content_css = 'tabpanel tab-pane'
            tab_content_css += ' active' if tab_count == 0 else ''
            tab_content_div = _html.Div('', css=tab_content_css, uid='tab-uid-' + tab_id)
            tabs_content.append(tab_content_div)

            for widget in sorted(tab['widgets'], key=lambda x: x.weight):
                tab_content_div.append(_html.TagLessElement(widget.render()))

            tab_count += 1

        return tab_panel


class Score(_base.Abstract):
    def __init__(self, uid: str, **kwargs):
        kwargs['default'] = kwargs.get('default', 3)

        super().__init__(uid, **kwargs)

        self._min = kwargs.get('min', 1)
        self._max = kwargs.get('max', 5)
        self._show_numbers = kwargs.get('show_numbers', True)

        self.css += ' widget-select-score'

        self._js_module = 'pytsite-widget-select-score'

    def _get_element(self, **kwargs) -> _html.Element:
        cont = _html.Div(css='switches-wrap')

        if self._enabled:
            cont.append(_html.Input(name=self.uid, type='hidden', value=self.get_val()))
            self.css += ' enabled'

        for i in range(self._min, self._max + 1):
            a = _html.Span(css='switch score-' + str(i), data_score=str(i))

            if self._show_numbers:
                a.content = str(i)

            if i == self.get_val():
                a.set_attr('css', a.get_attr('css') + ' active')

            cont.append(a)

        return cont


class TrafficLightScore(Score):
    def __init__(self, uid: str, **kwargs):
        """Hook.
        """
        kwargs['default'] = kwargs.get('default', 2)

        super().__init__(uid, max=3, show_numbers=False, **kwargs)

        self._css += ' widget-select-traffic-light-score'
        self._js_module = 'pytsite-widget-select-traffic-light-score'


class ColorPicker(_input.Text):
    def __init__(self, uid: str, **kwargs):
        """Hook.
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-color-picker'
        self._js_module = 'pytsite-widget-select-color-picker'

    def _get_element(self, **kwargs):
        self._data['color'] = self.value

        return super()._get_element()
