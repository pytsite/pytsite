"""PytSite Select Widgets.
"""
from datetime import datetime as _datetime
from pytsite import browser as _browser, html as _html, lang as _lang, validation as _validation, \
    hreflang as _hreflang, router as _router
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

    def _get_select_html_em(self) -> _html.Element:
        select = _html.Select(name=self.name, cls='form-control', required=self._required)
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
        super().__init__(uid, **kwargs)

        self.set_val(kwargs.get('value', []))

        if not isinstance(self._value, list):
            raise TypeError("List expected.")

        self._selected_items = kwargs.get('selected_items', self._value)

    def set_val(self, value: list, **kwargs):
        """Set value of the widget.
        """

        if not isinstance(value, list):
            raise TypeError('List expected')

        self._value = value
        self._selected_items = value

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        div = _html.Div()
        div.append(_html.Input(type='hidden', name=self.uid + '[]'))
        for item in self._items:
            checked = True if item[0] in self._selected_items else False
            div.append(
                _html.Div(cls='checkbox').append(
                    _html.Label(item[1]).append(
                        _html.Input(type='checkbox', name=self.uid + '[]', value=item[0], checked=checked)
                    )
                )
            )

        return self._group_wrap(div)


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


class LanguageNav(_base.Base):
    """Language Nav Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._bootstrap = kwargs.get('bootstrap', True)
        self._dropdown = kwargs.get('dropdown')
        self._css += ' lang-switch'

        if self._bootstrap:
            self._css += ' nav navbar-nav'

    def get_html_em(self, **kwargs) -> _html.Element:
        if len(_lang.langs()) == 1:
            return _html.TagLessElement()

        root_ul = _html.Ul(uid=self._uid, cls=self._css)
        cur_lang = _lang.get_current()

        if self._dropdown:
            # Dropdown menu
            dropdown_root = _html.Li(cls='dropdown')
            toggle_a = _html.A(_lang.lang_title(cur_lang), cls='dropdown-toggle lang-' + cur_lang,
                               data_toggle='dropdown', role='button',
                               aria_haspopup='true', aria_expanded='false', href='#', content_first=True)
            toggle_a.append(_html.Span(cls='caret'))

            dropdown_menu = _html.Ul(cls='dropdown-menu')
            for lng in _lang.langs(False):
                hl = _hreflang.get(lng)
                if hl:
                    dropdown_menu.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=hl))
                    )
                else:
                    # Link to homepage
                    dropdown_menu.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.base_url(lang=lng)))
                    )

            dropdown_root.append(toggle_a).append(dropdown_menu)
            root_ul.append(dropdown_root)
        else:
            # Simple list
            for lng in _lang.langs():
                lang_title = _lang.lang_title(lng)
                if lng == cur_lang:
                    # Active language
                    root_ul.append(_html.Li(cls='active').append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.current_url(),
                                title=lang_title)))
                elif _hreflang.get(lng):
                    # Inactive language, related link
                    root_ul.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_hreflang.get(lng),
                                title=lang_title)))
                else:
                    # Link to homepage, no related link found
                    root_ul.append(_html.Li().append(
                        _html.A(_lang.lang_title(lng), cls='lang-' + lng, href=_router.base_url(lang=lng),
                                title=lang_title)))

        return root_ul


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


class Score(_base.Base):
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
