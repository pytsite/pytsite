"""File Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path, unlink
from pytsite.core import odm, router, reg


class File(odm._model.ODMModel):
    """File Model.
    """

    def _setup(self):

        """_setup() hook.
        """
        self._define_field(odm._field.String('path', not_empty=True))
        self._define_field(odm._field.String('name', not_empty=True))
        self._define_field(odm._field.String('description'))
        self._define_field(odm._field.String('mime', not_empty=True))
        self._define_field(odm._field.Integer('length', not_empty=True))
        self._define_field(odm._field.Ref('author', model='user'))
        self._define_field(odm._field.Virtual('abs_path'))
        self._define_field(odm._field.Virtual('url'))
        self._define_field(odm._field.Virtual('thumb_url'))

    def _after_delete(self):
        """_after_delete() hook.
        """
        storage_dir = reg.get('paths.storage')
        file_abs_path = path.join(storage_dir, self.f_get('path'))
        if path.exists(file_abs_path):
            unlink(file_abs_path)

    def _on_f_get(self, field_name: str, orig_value, **kwargs):
        """_on_f_get() hook.
        """

        if field_name == 'abs_path':
            return path.join(reg.get('paths.storage'), self.f_get('path'))

        if field_name == 'url':
            p = str(self.f_get('path')).split('/')
            return router.endpoint_url('pytsite.file.eps.get_download', {
                'model': p[0],
                'p1': p[1],
                'p2': p[2],
                'filename': p[3]
            })

        if field_name == 'thumb_url':
            raise NotImplementedError()

        return super()._on_f_get(field_name, orig_value)
