"""Comments Models.
"""
from datetime import datetime as _datetime
from pytsite import auth as _auth, util as _util, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AbstractComment:
    @property
    def uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def parent_uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def thread_uid(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def depth(self) -> int:
        raise NotImplementedError("Not implemented yet")

    @property
    def created(self) -> _datetime:
        raise NotImplementedError("Not implemented yet")

    @property
    def url(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def body(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def publish_time(self) -> _datetime:
        raise NotImplementedError("Not implemented yet")

    @property
    def status(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def author(self) -> _auth.model.AbstractUser:
        raise NotImplementedError("Not implemented yet")

    @property
    def permissions(self) -> dict:
        raise NotImplementedError("Not implemented yet")

    @property
    def is_reply(self) -> bool:
        return bool(self.parent_uid)

    def as_jsonable(self) -> dict:
        r = {
            'uid': self.uid,
            'parent_uid': self.parent_uid,
            'thread_uid': self.thread_uid,
            'status': self.status,
            'depth': self.depth,
            'permissions': self.permissions,
            'publish_time': {
                'w3c': _util.w3c_datetime_str(self.publish_time),
                'pretty_date': _lang.pretty_date(self.publish_time),
                'pretty_date_time': _lang.pretty_date_time(self.publish_time),
                'ago': _lang.time_ago(self.publish_time),
            },
        }

        if self.status == 'published':
            author = self.author
            r.update({
                'body': self.body,
                'author': {
                    'uid': author.uid,
                    'nickname': author.nickname,
                    'full_name': author.full_name,
                    'picture_url': author.picture.get_url(width=50, height=50),
                    'profile_url': author.profile_view_url if author.profile_is_public else None,
                },
            })

        return r
