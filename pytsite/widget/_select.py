"""PytSite Select Widgets.
"""
from typing import Union as _Union, List as _List, Tuple as _Tuple
from math import ceil as _ceil
from datetime import datetime as _datetime
from pytsite import browser as _browser, html as _html, lang as _lang, validation as _validation, util as _util, \
    hreflang as _hreflang, router as _router, http_api as _http_api
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
        super().__init__(uid, **kwargs)
        self._label_disabled = True

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        self._value = bool(value)

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        div = _html.Div(cls='checkbox')
        div.append(_html.Input(type='hidden', name=self._name))
        label = _html.Label(self._label, label_for=self._uid)
        label.append(_html.Input(uid=self._uid, name=self._name, type='checkbox', checked=self._value))
        div.append(label)

        return self._group_wrap(div)


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
        select = _html.Select(name=self.name, cls='form-control', required=self._required)

        if self._append_none_item:
            select.append(_html.Option('--- ' + _lang.t('pytsite.widget@select_none_item') + ' ---', value=''))

        for item in self._items:
            option = _html.Option(item[1], value=item[0])
            if item[0] == self._value:
                option.set_attr('selected', True)
            select.append(option)

        return select

    def get_html_em(self, **kwargs):
        """Render the widget.
        :param **kwargs:
        """
        return self._group_wrap(self._get_select_html_em())


class Select2(Select):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self.assets.extend(_browser.get_assets('select2'))
        self.assets.extend(['pytsite.widget@js/select2.js'])

        self._theme = kwargs.get('theme', 'bootstrap')
        self._ajax_url = kwargs.get('ajax_url')
        self._ajax_delay = kwargs.get('ajax_delay', 750)
        self._ajax_data_type = kwargs.get('ajax_data_type', 'json')
        self._css += ' widget-select-select2'

    def get_html_em(self, **kwargs) -> _html.Element:
        select = self._get_select_html_em()
        select.set_attr('style', 'width: 100%;')

        if self._ajax_url:
            select.set_attr('data_theme', self._theme)
            select.set_attr('data_ajax_url', self._ajax_url)
            select.set_attr('data_ajax_delay', self._ajax_delay)
            select.set_attr('data_ajax_data_type', self._ajax_data_type)

        return self._group_wrap(select)


class Checkboxes(Select):
    """Group of Checkboxes Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = ()

        self._unique = kwargs.get('unique', False)

        super().__init__(uid, **kwargs)

        self._selected_items = kwargs.get('selected_items', self.get_val())

    def set_val(self, value: _Union[_List, _Tuple], **kwargs):
        """Set value of the widget.
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError('List or tuple expected.')

        super().set_val(_util.cleanup_list(value, self._unique))

        self._selected_items = self.get_val()

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        container = _html.TagLessElement()
        container.append(_html.Input(type='hidden', name=self.uid + '[]'))
        for item in self._items:
            checked = True if item[0] in self._selected_items else False
            container.append(
                _html.Div(cls='checkbox').append(
                    _html.Label(item[1]).append(
                        _html.Input(type='checkbox', name=self.uid + '[]', value=item[0], checked=checked)
                    )
                )
            )

        return self._group_wrap(container)


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
        self._dropdown = kwargs.get('dropdown')
        self._css += ' nav navbar-nav widget-select-language-nav'

    def get_html_em(self, **kwargs) -> _html.Element:
        if len(_lang.langs()) == 1:
            return _html.TagLessElement()

        root = _html.TagLessElement()

        # Dropdown menu
        if self._dropdown:
            # Root element
            dropdown_root = _html.Li(cls='dropdown')
            toggle_a = _html.A(
                _lang.lang_title(self.language),
                cls='dropdown-toggle lang-' + self.language,
                data_toggle='dropdown',
                role='button',
                aria_haspopup='true',
                aria_expanded='false',
                href='#',
                content_first=True)
            toggle_a.append(_html.Span(cls='caret'))

            # Children
            dropdown_menu = _html.Ul(cls='dropdown-menu')
            for lng in _lang.langs():
                # Skip current language
                if lng == self.language:
                    continue

                hl = _hreflang.get(lng)
                if hl:
                    dropdown_menu.append(
                        _html.Li().append(_html.A(_lang.lang_title(lng), cls='lang-' + lng, href=hl)))
                else:
                    # Link to homepage
                    dropdown_menu.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.base_url(lang=lng))))

            dropdown_root.append(toggle_a).append(dropdown_menu)
            root.append(dropdown_root)
        else:
            # Simple list
            for lng in _lang.langs():
                lang_title = _lang.lang_title(lng)
                if lng == self.language:
                    # Active language
                    root.append(_html.Li(cls='active').append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.current_url(),
                                title=lang_title)))
                elif _hreflang.get(lng):
                    # Inactive language, related link
                    root.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_hreflang.get(lng),
                                title=lang_title)))
                else:
                    # Link to homepage, no related link found
                    root.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.base_url(lang=lng),
                                title=lang_title)))

        return root


class DateTime(_input.Text):
    """Date/Time Select Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self.assets.extend(_browser.get_assets('datetimepicker'))
        self.assets.extend(['pytsite.widget@js/datetime.js'])

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

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget
        :param **kwargs:
        """
        html_input = _html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self.get_val().strftime('%d.%m.%Y %H:%M'),
            cls=' '.join(('form-control', self._css)),
            required=self._required,
        )

        return self._group_wrap(html_input)


class Pager(_base.Abstract):
    """Pager Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._total_items = int(kwargs.get('total_items'))
        if self._total_items is None:
            raise ValueError("'total_items' is required argument.")

        self._items_per_page = int(kwargs.get('per_page', 100))
        self._total_pages = _ceil(self._total_items / self._items_per_page)
        self._visible_numbers = int(kwargs.get('visible_numbers', 5)) - 1
        self._ajax = kwargs.get('ajax', '')

        # Detect current page
        try:
            self._current_page = int(_router.request().inp.get('page', 1))
        except ValueError:
            self._current_page = 1

        if self._current_page > self._total_pages:
            self._current_page = self._total_pages
        if self._current_page < 1:
            self._current_page = 1

        self._data['ajax'] = self._ajax
        self._data['current_page'] = self._current_page
        self._data['per_page'] = self._items_per_page

        self.assets.extend([
            'pytsite.widget@js/pager.js'
        ])

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
        links_url = _http_api.url(self._ajax) if self._ajax else _router.current_url()

        if start_visible_num > 1:
            # Link to the first page
            li = _html.Li(cls='first-page')
            a = _html.A('«', title=_lang.t('pytsite.widget@first_page'), data_page=1,
                        href=_router.url(links_url, query={'page': 1}))
            ul.append(li.append(a))

            # Link to the previous page
            li = _html.Li(cls='previous-page')
            a = _html.A('‹', title=_lang.t('pytsite.widget@previous_page'), data_page=self._current_page - 1,
                        href=_router.url(links_url, query={'page': self._current_page - 1}))
            ul.append(li.append(a))

        # Links to visible pages
        for num in range(start_visible_num, end_visible_num + 1):
            li = _html.Li()
            if self._current_page == num:
                li.set_attr('cls', 'active')
            a = _html.A(str(num), data_page=num, href=_router.url(links_url, query={'page': num}))
            ul.append(li.append(a))

        if end_visible_num < self._total_pages:
            # Link to the next page
            li = _html.Li(cls='next-page')
            a = _html.A('›', title=_lang.t('pytsite.widget@next_page'), data_page=self._current_page + 1,
                        href=_router.url(links_url, query={'page': self._current_page + 1}))
            ul.append(li.append(a))

            # Link to the last page
            li = _html.Li(cls='last-page')
            a = _html.A('»', title=_lang.t('pytsite.widget@last_page'), data_page=self._total_pages,
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


class Score(_base.Abstract):
    def __init__(self, uid: str, **kwargs):
        kwargs['default'] = kwargs.get('default', 3)

        super().__init__(uid, **kwargs)

        self._min = kwargs.get('min', 1)
        self._max = kwargs.get('max', 5)
        self._show_numbers = kwargs.get('show_numbers', True)

        self.css += ' widget-select-score'

        self.assets.extend([
            'pytsite.widget@css/score.css',
            'pytsite.widget@js/score.js',
        ])

    def get_html_em(self, **kwargs) -> _html.Element:
        cont = _html.Div(cls='switches-wrap')

        if self._enabled:
            cont.append(_html.Input(name=self.uid, type='hidden', value=self.get_val()))
            self.css += ' enabled'

        for i in range(self._min, self._max + 1):
            a = _html.Span(cls='switch score-' + str(i), data_score=str(i))

            if self._show_numbers:
                a.content = str(i)

            if i == self.get_val():
                a.set_attr('cls', a.get_attr('cls') + ' active')

            cont.append(a)

        return self._group_wrap(cont)


class TrafficLightScore(Score):
    def __init__(self, uid: str, **kwargs):
        """Hook.
        """
        kwargs['default'] = kwargs.get('default', 2)

        super().__init__(uid, max=3, show_numbers=False, **kwargs)

        self.css += ' widget-select-traffic-light-score'

        self.assets.extend([
            'pytsite.widget@css/traffic-light-score.css',
            'pytsite.widget@js/traffic-light-score.js',
        ])
