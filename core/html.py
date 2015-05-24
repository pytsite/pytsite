__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC
from .util import xml_attrs_str

_common_tag_attrs = (
    'accesskey',
    'cls',
    'contenteditable',
    'contextmenu',
    'dir',
    'draggable',
    'dropzone',
    'hidden',
    'id',
    'lang',
    'spellcheck',
    'style',
    'tabindex',
    'title',
    'translate'
)


class Element(ABC):
    def __init__(self, content: str=None, **kwargs):
        self._tag_name = self.__class__.__name__.lower()
        self._content = content
        self._children = []
        self._attrs = {}

        for k, v in kwargs.items():
            self.set_attr(k, v)

        for attr in self._get_required_attrs():
            if attr not in self._attrs:
                raise AttributeError("Required attribute '{0}' is not specified for element '{1}'.".
                                     format(attr, self.tag_name))

    @property
    def tag_name(self):
        return self._tag_name

    @property
    def content(self):
        return self._content

    def set_attr(self, attr: str, value: str):
        """Set attribute.
        """

        if attr not in _common_tag_attrs and not attr.startswith('data_') and attr not in self._get_valid_attrs():
            raise AttributeError("Element '{0}' cannot have attribute: '{1}'".format(self._tag_name, attr))

        if attr.startswith('data_'):
            attr = attr.replace('_', '-')

        self._attrs[attr] = self._validate_attr(attr, value)

        return self

    def get_attr(self, attr):
        """Get attribute.
        """

        if attr not in _common_tag_attrs:
            raise KeyError("Attribute '{0}' is not defined.".format(attr))
        return self._attrs[attr]

    def append(self, child):
        """Append child.
        """

        if not isinstance(child, Element):
            raise TypeError("Element expected.")

        valid_children = self._get_valid_children()

        if isinstance(valid_children, str):
            if valid_children == 'any_inline' and not isinstance(child, InlineElement):
                raise ValueError("Element '{0}' cannot be child of '{1}'".format(child.tag_name, self.tag_name))
            if valid_children == 'any_block' and not isinstance(child, BlockElement):
                raise ValueError("Element '{0}' cannot be child of '{1}'".format(child.tag_name, self.tag_name))
        elif isinstance(valid_children, tuple) and child.tag_name not in self._get_valid_children():
                raise ValueError("Element '{0}' cannot be child of '{1}'".format(child.tag_name, self.tag_name))

        self._children.append(self._validate_child(child))

        return self

    def _validate_attr(self, attr: str, value: str) -> str:
        return value

    def _get_valid_attrs(self) -> tuple:
        return ()

    def _get_required_attrs(self) -> tuple:
        return ()

    def _validate_child(self, child):
        return child

    def _get_valid_children(self) -> tuple:
        return ()

    def render(self) -> str:
        """Render the element.
        """

        # Open tag
        r = "<{}{}>".format(self._tag_name, xml_attrs_str(self._attrs, {
            'cls': 'class',
            'label_for': 'for',
        }))

        # Render children
        if self._children:
            for child in self._children:
                r += str(child)

        # Element's content
        if self._content:
            if self._children:
                r += '&nbsp;'
            r += self._content

        # Close tag
        r += "</{}>".format(self._tag_name)

        return r

    def __str__(self) -> str:
        """Render the element.
        """
        return self.render()


class SingleTagElement(Element):
    """Element without closing tag.
    """

    def _validate_child(self, child):
        raise ValueError("'{}' element cannot contain children.".format(self._tag_name))

    def render(self) -> str:
        """Render the element.
        """

        return "<{}{}>".format(self._tag_name, xml_attrs_str(self._attrs, {'cls': 'class'}))


class InlineElement(Element):
    """Inline element.
    """

    def _get_valid_children(self):
        return 'any_inline'


class BlockElement(Element):
    """Block element.
    """

    def _get_valid_children(self):
        return 'any'


class Span(InlineElement):
    pass


class B(Span):
    pass


class Strong(B):
    pass


class I(Span):
    pass


class Button(Span):
    def _get_valid_attrs(self) -> tuple:
        return 'type',

    def _get_required_attrs(self):
        return 'type',


class A(Span):
    def _get_required_attrs(self):
        return 'href',

    def _get_valid_attrs(self):
        return 'href',


class Img(InlineElement, SingleTagElement):
    def _get_valid_attrs(self) -> tuple:
        return 'src', 'width', 'height'

    def _get_required_attrs(self):
        return 'src',


class Div(BlockElement):
    pass


class Section(Div):
    pass


class Header(Section):
    pass


class Footer(Section):
    pass


class Aside(Section):
    pass


class P(BlockElement):
    pass


class Ul(BlockElement):
    def _get_valid_children(self):
        return 'li',


class Ol(Ul):
    pass


class Li(Span):
    pass


class Table(BlockElement):
    def _get_valid_children(self):
        return 'thead', 'tbody', 'tfoot', 'tr'


class THead(BlockElement):
    def _get_valid_children(self):
        return 'tr',


class TBody(BlockElement):
    def _get_valid_children(self):
        return 'tr',


class TFoot(BlockElement):
    def _get_valid_children(self):
        return 'tr',


class Tr(BlockElement):
    def _get_valid_children(self):
        return 'td', 'th'


class Td(BlockElement):
    def _get_valid_attrs(self):
        return 'colspan', 'rowspan'

    def _get_valid_children(self):
        return 'any'


class Th(Td):
    pass


class Form(BlockElement):
    pass


class Input(InlineElement, SingleTagElement):
    def _get_valid_attrs(self) -> tuple:
        return 'name', 'type', 'value', 'placeholder'


class TextArea(BlockElement):
    pass


class Label(InlineElement):
    def _get_valid_attrs(self) -> tuple:
        return 'label_for',


class Select(BlockElement):
    def _get_valid_children(self):
        return 'option',


class Option(InlineElement):
    def _get_required_attrs(self):
        return 'value',
