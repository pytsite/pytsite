"""PytSite Base Widget.
"""
from json import dumps as _json_dumps
from typing import Iterable as _Iterable, Tuple as _Tuple, List as _List
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from copy import deepcopy as _deepcopy
from pytsite import html as _html, validation as _validation, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Abstract Base Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        self._uid = uid
        self._wrap_em = _html.Div()
        self._name = kwargs.get('name', uid)
        self._language = kwargs.get('language', _lang.get_current())
        self._weight = kwargs.get('weight', 0)
        self._default = kwargs.get('default')
        self._value = None  # Wil be set later
        self._label = kwargs.get('label')
        self._title = kwargs.get('title')
        self._label_hidden = kwargs.get('label_hidden', False)
        self._label_disabled = kwargs.get('label_disabled', False)
        self._placeholder = kwargs.get('placeholder')
        self._css = kwargs.get('css', '')
        self._data = kwargs.get('data', {})
        self._has_success = kwargs.get('has_success', False)
        self._has_warning = kwargs.get('has_warning', False)
        self._has_error = kwargs.get('has_error', False)
        self._help = kwargs.get('help')
        self._h_size = kwargs.get('h_size')
        self._hidden = kwargs.get('hidden', False)
        self._rules = kwargs.get('rules', [])  # type: _List[_validation.rule.Rule]
        self._form_area = kwargs.get('form_area', 'body')
        self._js_module = kwargs.get('js_module', '')
        self._replaces = kwargs.get('replaces')
        self._required = kwargs.get('required', False)
        self._enabled = kwargs.get('enabled', True)
        self._parent = kwargs.get('parent')
        self._child_sep = kwargs.get('child_sep', '')
        self._children = []  # type: _List[Abstract]
        self._children_uids = []  # type: _List[str]
        self._group_wrap = True

        # Check validation rules
        if not isinstance(self._rules, (list, tuple)):
            self._rules = [self._rules]
        if isinstance(self._rules, tuple):
            self._rules = list(self._rules)
        for rule in self._rules:
            if not isinstance(rule, _validation.rule.Rule):
                raise TypeError('Instance of pytsite.validation.rule.Base expected.')

        if self.required:
            self.add_rule(_validation.rule.NonEmpty())

        if 'value' in kwargs:
            # It is important to filter value through the setter-method
            self.set_val(kwargs.get('value'), mode='init')
        else:
            self._value = _deepcopy(self._default)

    @_abstractmethod
    def _get_element(self, **kwargs) -> _html.Element:
        """Hook.
        """
        pass

    def get_element(self, **kwargs) -> _html.Element:
        """Get an HTML element representation of the widget.
        """
        # Wrapper div
        self._wrap_em.set_attr('data_cid', self.__module__ + '.' + self.__class__.__name__)
        self._wrap_em.set_attr('data_uid', self._uid)
        self._wrap_em.set_attr('data_weight', self._weight)
        self._wrap_em.set_attr('data_form_area', self._form_area)
        self._wrap_em.set_attr('data_hidden', self._hidden)
        self._wrap_em.set_attr('data_enabled', self._enabled)
        self._wrap_em.set_attr('data_parent_uid', self._parent.uid if self._parent else None)

        # JS modules to load with widget initialization
        if self._js_module:
            self._wrap_em.set_attr('data_js_module', self._js_module)

        # Replaces
        if self._replaces:
            self._wrap_em.set_attr('data_replaces', self._replaces)

        # Get widget's HTML element
        em = self._get_element(**kwargs)

        # Wrapper CSS
        wrap_css = 'pytsite-widget widget-uid-{} {}'.format(self._uid, self._css)
        if self._hidden:
            wrap_css += ' hidden'
        self._wrap_em.set_attr('css', wrap_css)

        # Data attributes
        if isinstance(self._data, dict):
            for k, v in self._data.items():
                self._wrap_em.set_attr('data_' + k, v)

        # Wrap into 'form-group' div
        if self._group_wrap:
            em = self._wrap_into_group(em)

        # Wrap widget's HTML
        self._wrap_em.append(em)

        return self._wrap_em

    def render(self, **kwargs) -> str:
        """Render the widget into a string.
        """
        return self.get_element(**kwargs).render()

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return "{}.{}(uid='{}', name='{}')".format(__name__, self.__class__.__name__, self.uid, self.name)

    def get_val(self, **kwargs):
        """Get value of the widget.
        """
        return self._value

    @property
    def default(self):
        return self._default

    @property
    def value(self):
        """Shortcut for get_value().
        """
        return self.get_val()

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        self._value = value if value is not None else _deepcopy(self._default)

        return self

    @value.setter
    def value(self, val):
        """Shortcut for set_value().
        """
        self.set_val(val)

    def clr_val(self):
        self._value = _deepcopy(self._default)

    def hide(self):
        """Hides the widget.
        """
        self._hidden = True

        return self

    def show(self):
        """Shows the widget.
        """
        self._hidden = False

        return self

    @property
    def uid(self) -> str:
        """Get UID of the widget.
        """
        return self._uid

    @uid.setter
    def uid(self, value):
        """Set UID of the widget.
        """
        self._uid = value

    @property
    def name(self) -> str:
        """Get name of the widget.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, value: str):
        self._language = value

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: int):
        self._weight = int(value)

    @property
    def label(self) -> str:
        """Get label of the widget.
        """
        return self._label

    @label.setter
    def label(self, value: str):
        """Set label of the widget.
        """
        self._label = value

    @property
    def title(self) -> str:
        """Get title of the widget.
        """
        return self._title

    @title.setter
    def title(self, value: str):
        """Set title of the widget.
        """
        self._title = value

    @property
    def placeholder(self):
        """Get placeholder of the widget.
        """
        return self._placeholder

    @property
    def css(self) -> str:
        """Get CSS classes of the widget.
        """
        return self._css

    @css.setter
    def css(self, value):
        self._css = value

    @property
    def has_success(self):
        """Get has_success property of the widget.
        """
        return self._has_success

    @has_success.setter
    def has_success(self, value: str):
        """Set has_success property of the widget.
        """
        self._has_success = value

    @property
    def has_warning(self):
        """Get has_warning property of the widget.
        """
        return self._has_warning

    @has_warning.setter
    def has_warning(self, value: str):
        """Set has_warning property of the widget.
        """
        self._has_warning = value

    @property
    def has_error(self):
        """Get has_error property of the widget.
        """
        return self._has_error

    @has_error.setter
    def has_error(self, value: str):
        """Set has_error property of the widget.
        """
        self._has_error = value

    @property
    def help(self):
        """Get help string of the widget.
        """
        return self._help

    @help.setter
    def help(self, value: str):
        """Set help string of the widget.
        """
        self._help = value

    @property
    def form_area(self) -> str:
        return self._form_area

    @form_area.setter
    def form_area(self, area: str):
        self._form_area = area

    @property
    def h_size(self) -> str:
        return self._h_size

    @h_size.setter
    def h_size(self, value: str):
        self._h_size = value

    @property
    def js_module(self) -> str:
        """Get CSS files list.
        """
        return self._js_module

    @property
    def replaces(self) -> str:
        return self._replaces

    @replaces.setter
    def replaces(self, value: str):
        self._replaces = value

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(_validation.rule.NonEmpty())
        else:
            # Clear all added NonEmpty rules
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, _validation.rule.NonEmpty)])

        self._required = value

    @property
    def parent(self):
        """
        :rtype: pytsite.widget.Container
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        """
        :type value: pytsite.widget.Container
        """
        self._parent = value

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    @property
    def children(self):
        """Get children widgets.

        :rtype: _List[Abstract]
        """
        return self._children

    @property
    def group_wrap(self) -> bool:
        return self._group_wrap

    @group_wrap.setter
    def group_wrap(self, value: bool):
        self._group_wrap = value

    def has_child(self, uid: str) -> bool:
        """Check if the widget has a child.
        """
        return uid in self._children_uids

    def has_descendant(self, uid: str) -> bool:
        """Check if the widget has a child.
        """
        for w in self._children:
            if w.uid == uid:
                return True
            else:
                return w.has_descendant(uid)

        return False

    def append_child(self, widget):
        """Append a child widget.

        :type widget: Abstract
        :rtype: Abstract
        """
        if self.has_descendant(widget.uid):
            raise RuntimeError("Widget '{}' already contains descendant '{}'.".format(self.uid, widget.uid))

        widget.form_area = self.form_area
        widget.parent = self

        self._children.append(widget)
        self._children_uids.append(widget.uid)
        self._children.sort(key=lambda x: x.weight)

        return widget

    def get_child(self, uid: str):
        """Get child widget by uid.

        :rtype: Abstract
        """
        if not self.has_child(uid):
            raise RuntimeError("Widget '{}' doesn't contain child '{}'.".format(self.uid, uid))

        for w in self._children:
            if w.uid == uid:
                return w

    def remove_child(self, uid: str):
        """Remove child widget.
        """
        if not self.has_child(uid):
            raise RuntimeError("Widget '{}' doesn't contain child '{}'.".format(self.uid, uid))

        self._children = [w for w in self._children if w.uid != uid]

        return self

    def add_rule(self, rule: _validation.rule.Rule):
        """Add single validation rule.
        """
        self._rules.append(rule)

        return self

    def add_rules(self, rules: _Iterable):
        """Add multiple validation rules.
        """
        for rule in rules:
            self.add_rule(rule)

        return self

    def get_rules(self) -> _Tuple[_validation.rule.Rule]:
        """Get validation rules.
        """
        return tuple(self._rules)

    def clr_rules(self):
        """Clear validation rules.
        """
        self._rules = []

        return self

    def validate(self):
        """Validate the widget's rules.
        """
        for rule in self.get_rules():
            rule.validate(self.get_val(mode='validation'))

    def _wrap_into_group(self, content) -> _html.Element:
        """Wraps a widget, an HTML element or a string into 'form-group' container.

        :type content: pytsite.widget._base.Abstract | pytsite.html.Element | str
        """
        if isinstance(content, str):
            content = _html.TagLessElement(content)
        elif isinstance(content, Abstract):
            content = content._get_element()

        if self._h_size:
            content = content.wrap(_html.Div(css='h-sizer ' + self._h_size))
            content = content.wrap(_html.Div(css='row'))

        wrap_css = 'form-group'
        if self._has_success:
            wrap_css += ' has-success'
        if self._has_warning:
            wrap_css += ' has-warning'
        if self._has_error:
            wrap_css += ' has-error'
        wrap = _html.Div(css=wrap_css)

        # Place placeholder instead of label
        if not self._label and self._placeholder:
            self._label = self.placeholder

        # Append label element
        if self.label and not self._label_disabled:
            label = _html.Label(self.label, label_for=self.uid)
            if self._label_hidden:
                label.set_attr('css', 'sr-only')
            wrap.append(label)

        # Append widget's content
        wrap.append(content)

        # Append help block
        if self._help:
            wrap.append(_html.Span(self._help, css='help-block'))

        # Append messages placeholder
        wrap.append(_html.Div(css='widget-messages'))

        return wrap


class Container(Abstract):
    """Simple Container Widget.
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._group_wrap = False
        self._css += ' widget-container'

    def validate(self):
        """Validate widget's rules.
        """
        for w in self.children:
            for rule in w.get_rules():
                rule.validate(w.get_val(mode='validation'))

    def _get_element(self, **kwargs) -> _html.Element:
        cont = _html.TagLessElement(child_sep=self._child_sep)

        for w in self.children:
            cont.append(w.get_element())

        return cont


class MultiRow(Abstract):
    """Multi Row Widget.
    """

    def __init__(self, uid: str, **kwargs):
        self._add_btn_title = kwargs.get('add_btn_title', _lang.t('pytsite.widget@append'))

        super().__init__(uid, **kwargs)

        self._css += ' widget-multi-row'
        self._js_module = 'pytsite-widget-multi-row'

    def append_child(self, widget: Abstract):
        raise NotImplementedError('This widget can not contain children')

    @property
    def children(self):
        raise NotImplementedError('This widget can not contain children')

    def set_val(self, value: list, **kwargs):
        if value is None:
            value = []

        # If value comes from HTTP input, it usually would be a dict, and it should be converted to a list
        if isinstance(value, dict):
            new_val = []
            keys = list(value.keys())
            val_len = len(value[keys[0]])
            for n in range(0, val_len):
                new_val_item = {}
                for k in keys:
                    new_val_item[k] = value[k][n]
                new_val.append(new_val_item)

            value = new_val

        # Check type of the entire value
        if not isinstance(value, list):
            raise TypeError('List expected, {} given'.format(type(value)))

        # Cleanup value
        clean_value = []
        for v in value:
            if not isinstance(v, dict):
                raise TypeError('Dict expected, {} given'.format(type(v)))

            # Check that all values of the dict is not empty
            clean_v_values = [v_value for v_value in v.values() if v_value]
            if clean_v_values:
                clean_value.append(v)
        value = clean_value

        # Create child widgets based on value
        self._children = []
        for value_item in value:
            children_row = []
            for w in self._get_widgets_row():
                if not isinstance(w, Abstract):
                    raise TypeError('Widget expected, {} given'.format(type(w)))

                w.value = value_item[w.name] if w.name in value_item else None
                children_row.append(w)

            self._children.append(children_row)

        super().set_val(value)

    def validate(self):
        """Validate widget's rules.
        """
        row_i = 0
        for row in self._children:
            widget_i = 0
            for w in row:
                for rule in w.get_rules():
                    try:
                        rule.validate(w.get_val(mode='validation'))
                    except _validation.error.RuleError as e:
                        msg_id = 'pytsite.widget@multi_row_validation_error'
                        msg_args = {
                            'row_index': row_i + 1,
                            'widget_title': self._get_headers_row()[widget_i],
                            'orig_msg': str(e)
                        }

                        raise _validation.error.RuleError(msg_id, msg_args)

                widget_i += 1

            row_i += 1

    @_abstractmethod
    def _get_headers_row(self) -> list:
        """Hook.
        """
        pass

    @_abstractmethod
    def _get_widgets_row(self) -> list:
        """Hook.
        """
        pass

    def _get_element(self, **kwargs) -> _html.Element:
        def _build_row(widgets: _List[Abstract], k: int = 0, add_css: str='') -> _html.Tr:
            slot_tr = _html.Tr(css='slot ' + add_css)
            slot_tr.append(_html.Td('[{}]'.format(k + 1), css='order-col'))

            # Widgets
            for w in widgets:
                w.name = '{}[{}][]'.format(self.name, w.name)
                w.group_wrap = False
                w.css += ' widget-row-col'

                w_td = _html.Td(css='widget-col')
                w_td.append(w.get_element())

                slot_tr.append(w_td)

            # Actions
            actions_td = _html.Td(css='actions-col')
            remove_btn = _html.A(href='#', css='button-remove-slot btn btn-xs btn-danger')
            remove_btn.append(_html.I(css='fa fa-icon fa-remove'))
            actions_td.append(remove_btn)
            slot_tr.append(actions_td)

            return slot_tr

        table = _html.Table(css='content-table')

        # Header
        thead = _html.THead(css='hidden slots-header')
        table.append(thead)
        row = _html.Tr()
        thead.append(row)
        row.append(_html.Th('#', css='order-col'))
        for v in self._get_headers_row():
            row.append(_html.Th(v, css='widget-col'))
        row.append(_html.Th(css='widget-col'))

        # Table body
        tbody = _html.TBody(css='slots')
        table.append(tbody)

        # Sample slot
        sample_row = self._get_widgets_row()
        tbody.append(_build_row(sample_row, add_css='sample hidden'))

        # Rows
        for i in range(0, len(self._children)):
            tbody.append(_build_row(self._children[i], i))

        # Footer
        tfoot = _html.TFoot()
        tr = _html.Tr()
        td = _html.Td(colspan=len(self._get_widgets_row()) + 2)
        add_btn = _html.A(self._add_btn_title or '', href='#', css='button-add-slot btn btn-default btn-xs')
        add_btn.append(_html.I(css='fa fa-plus'))
        td.append(add_btn)
        tr.append(td)
        tfoot.append(tr)
        table.append(tfoot)

        return table
