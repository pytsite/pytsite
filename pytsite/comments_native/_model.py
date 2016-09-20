"""Comments Models.
"""
from typing import Tuple as _Tuple
from datetime import datetime as _datetime
from pytsite import odm as _odm, odm_ui as _odm_ui, comments as _comments, auth as _auth, router as _router, \
    auth_storage_odm as _auth_storage_odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comment(_comments.model.AbstractComment, _odm_ui.model.UIEntity):
    def _setup_fields(self):
        """Setup fields.
        """
        valid_statuses = tuple(_comments.get_comment_statuses().keys())
        min_body_len = _comments.get_comment_body_min_length()
        max_body_len = _comments.get_comment_body_max_length()

        self.define_field(_odm.field.String('thread_uid', required=True))
        self.define_field(_odm.field.Enum('status', required=True, default='published', valid_values=valid_statuses))
        self.define_field(_odm.field.String('body', required=True, strip_html=True, min_length=min_body_len,
                                            max_length=max_body_len))
        self.define_field(_odm.field.DateTime('publish_time', required=True, default=_datetime.now()))
        self.define_field(_auth_storage_odm.field.User('author', required=True))

    def _setup_indexes(self):
        """Setup indexes.
        """
        self.define_index([('thread_uid', _odm.I_ASC), ('status', _odm.I_ASC)])
        self.define_index([('publish_time', _odm.I_ASC)])
        self.define_index([('author', _odm.I_ASC)])

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        return 'comments'

    @classmethod
    def odm_auth_permissions(cls) -> _Tuple[str]:
        return 'create', 'modify', 'delete', 'modify_own', 'delete_own'

    @property
    def uid(self) -> str:
        return str(self.id)

    @property
    def parent_uid(self) -> str:
        return str(self.parent.id) if self.parent else None

    @property
    def thread_uid(self) -> str:
        return self.f_get('thread_uid')

    @property
    def depth(self) -> int:
        return _odm_ui.model.UIEntity.depth.fget(self)

    @property
    def created(self) -> _datetime:
        return _odm_ui.model.UIEntity.created.fget(self)

    @property
    def url(self) -> str:
        return _router.url(self.f_get('thread_uid'), fragment='comment-' + self.uid)

    @property
    def body(self) -> str:
        return self.f_get('body')

    @property
    def publish_time(self) -> _datetime:
        return self.f_get('publish_time')

    @property
    def status(self) -> str:
        return self.f_get('status')

    @property
    def author(self) -> _auth.model.AbstractUser:
        return self.f_get('author')

    @property
    def permissions(self) -> dict:
        return {
            'modify': self.check_permissions('modify'),
            'delete': self.check_permissions('delete'),
        }
