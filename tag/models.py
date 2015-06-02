"""Tag Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.taxonomy.models import AbstractTerm


class Tag(AbstractTerm):
    """Tag Model.
    """

    def get_lang_package(self) -> str:
        """Get language package name.
        """
        return 'pytsite.tag'

    def get_permission_group(self) -> tuple:
        """Get permission group.
        """
        return 'tag', 'pytsite.tag@tag_plural_two'
