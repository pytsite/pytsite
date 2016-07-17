"""Abstract XML Based Feed.
"""
from lxml import etree as _etree
from . import _abstract

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Serializable(_abstract.Serializable):
    """XML Serializable.
    """

    def __init__(self, text: str = '', **kwargs):
        super().__init__()

        if not isinstance(text, str):
            text = str(text)

        self._text = text
        self._nsmap = kwargs.get('nsmap')

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def attributes(self) -> dict:
        return None

    @property
    def text(self) -> str:
        return self._text

    def get_content(self) -> _etree.Element:
        """Get object's content ready to serialization.
        """
        for r_child in self.required_children:
            if r_child not in self._children_names:
                raise KeyError("Element '{}' must have at least one '{}' child.".format(self.name, r_child))

        try:
            em = _etree.Element(self.name, self.attributes, self._nsmap)
        except TypeError as e:
            raise TypeError("Unexpected error while creating XML element '{}' with attributes '{}': {}".
                            format(self.name, self.attributes, e))

        if self.get_children():
            for child in self.get_children():
                em.append(child.get_content())
        else:
            em.text = self._text

        return em
