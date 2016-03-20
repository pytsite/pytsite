"""Comments Models.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class CommentsCount(_odm.Entity):
    """Comments Count Model.
    """
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('driver', nonempty=True))
        self.define_field(_odm.field.String('thread_id', nonempty=True))
        self.define_field(_odm.field.Integer('count'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('driver', _odm.I_ASC), ('thread_id', _odm.I_ASC)], unique=True)

    @property
    def driver(self) -> str:
        return self.f_get('driver')

    @property
    def thread_id(self) -> str:
        return self.f_get('thread_id')

    @property
    def count(self) -> int:
        return self.f_get('count')
