"""File Model.
"""
from os import path as _path, unlink as _unlink
from pytsite import odm as _odm, reg as _reg, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class File(_odm.Entity):
    """File Model.
    """

    def _setup_fields(self):
        """_setup() hook.
        """
        self.define_field(_odm.field.String('path', nonempty=True))
        self.define_field(_odm.field.String('name', nonempty=True))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.String('mime', nonempty=True))
        self.define_field(_odm.field.Integer('length', nonempty=True))
        self.define_field(_odm.field.Ref('owner', model='user'))
        self.define_field(_odm.field.Ref('attached_to'))
        self.define_field(_odm.field.Virtual('abs_path'))
        self.define_field(_odm.field.Virtual('url'))
        self.define_field(_odm.field.Virtual('thumb_url'))

    @property
    def path(self) -> str:
        return self.f_get('path')

    @property
    def abs_path(self) -> str:
        return self.f_get('abs_path')

    @property
    def url(self) -> str:
        return self.f_get('url')

    @property
    def thumb_url(self) -> str:
        return self.f_get('thumb_url')

    @property
    def name(self) -> str:
        return self.f_get('name')

    @property
    def length(self) -> int:
        return self.f_get('length')

    @property
    def mime(self) -> str:
        return self.f_get('mime')

    def _after_delete(self):
        """_after_delete() hook.
        """
        storage_dir = _reg.get('paths.storage')
        file_abs_path = _path.join(storage_dir, self.f_get('path'))
        if _path.exists(file_abs_path):
            _unlink(file_abs_path)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """_on_f_get() hook.
        """
        if field_name == 'abs_path':
            return _path.join(_reg.get('paths.storage'), self.path)

        if field_name == 'url':
            p = str(self.path).split('/')
            return _router.ep_url('pytsite.file.ep.download', {
                'model': p[0],
                'p1': p[1],
                'p2': p[2],
                'filename': p[3]
            })

        if field_name == 'thumb_url':
            raise NotImplementedError()

        return super()._on_f_get(field_name, value)
