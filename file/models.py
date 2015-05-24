"""File Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import odm


class File(odm.models.ODMModel):
    """File Model.
    """

    def get_thumbnail_url(self, width: int=64, height: int=64) -> str:
        """Get thumbnail URL.
        """
        raise NotImplementedError()

    def _setup(self):

        """_setup() hook.
        """
        self.define_field(odm.fields.StringField('path'))
        self.define_field(odm.fields.VirtualField('abs_path'))
        self.define_field(odm.fields.StringField('name'))
        self.define_field(odm.fields.StringField('description'))
        self.define_field(odm.fields.StringField('mime'))
        self.define_field(odm.fields.IntegerField('length'))
        self.define_field(odm.fields.RefField('author', model='user'))

    def _after_delete(self):
        """_after_delete() hook.
        """

        from os import path, unlink
        from ..core import reg
        storage_dir = reg.get('paths.storage')
        file_abs_path = path.join(storage_dir, self.f_get('path'))
        if path.exists(file_abs_path):
            unlink(file_abs_path)

    def _on_f_get(self, field_name: str, orig_value, **kwargs):
        """_on_f_get() hook.
        """

        if field_name == 'abs_path':
            from os import path
            from ..core import reg
            return path.join(reg.get('paths.storage'), self.f_get('path'))

        return super()._on_f_get(field_name, orig_value)
