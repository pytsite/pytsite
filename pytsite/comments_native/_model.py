"""Comments Models.
"""
from typing import Tuple as _Tuple
from pytsite import odm as _odm, odm_ui as _odm_ui, comments as _comments, image as _image, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comment(_comments.model.Comment, _odm_ui.model.UIEntity):
    def _setup_fields(self):
        """Setup fields.
        """
        self.define_field(_odm.field.String('thread_id', nonempty=True))
        self.define_field(_odm.field.String('body', nonempty=True))
        self.define_field(_odm.field.RefsUniqueList('images', model='images'))
        self.define_field(_odm.field.String('status', nonempty=True, default='published'))
        self.define_field(_odm.field.Ref('author', model='user', nonempty=True))

    def _setup_indexes(self):
        """Setup indexes.
        """
        self.define_index([('thread_id', _odm.I_ASC)])
        self.define_index([('author', _odm.I_ASC)])

    def _on_f_set(self, field_name: str, value, **kwargs):
        if field_name == 'status':
            if value not in _comments.get_comment_statuses():
                raise _comments.error.InvalidCommentStatus("'{}' is not a valid comment's status.".format(value))

        return value

    @property
    def thread_id(self) -> str:
        return self.f_get('thread_id')

    @property
    def body(self) -> str:
        return self.f_get('body')

    @property
    def images(self) -> _Tuple[_image.model.Image]:
        return self.f_get('images')

    @property
    def status(self) -> str:
        return self.f_get('status')

    @property
    def author(self) -> _auth.model.User:
        return self.f_get('author')
