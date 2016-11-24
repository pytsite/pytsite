"""PytSite Comments API.
"""
from typing import Dict as _Dict, Iterable as _Iterable
from frozendict import frozendict as _frozendict
from pytsite import router as _router, widget as _widget, auth as _auth, reg as _reg, lang as _lang, cache as _cache, \
    mail as _mail, tpl as _tpl, events as _events
from . import _driver, _error, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_last_registered_driver_name = None  # type: str
_drivers = {}  # type: _Dict[str, _driver.Abstract]
_comments_count = _cache.create_pool('pytsite.comments.count')
_comment_max_depth = int(_reg.get('comments.max_depth', 4))
_comment_body_min_length = int(_reg.get('comments.body_min_length', 2))
_comment_body_max_length = int(_reg.get('comments.body_max_length', 2048))


def register_driver(driver: _driver.Abstract):
    """Registers a comments driver.
    """
    global _drivers

    if not isinstance(driver, _driver.Abstract):
        raise TypeError("Instance of 'pytsite.comments.driver.Abstract' expected.")

    driver_name = driver.get_name()

    if driver_name in _drivers:
        raise _error.DriverAlreadyRegistered("Driver '{}' is already registered".format(driver_name))

    _drivers[driver_name] = driver

    global _last_registered_driver_name
    _last_registered_driver_name = driver_name


def get_drivers() -> _frozendict:
    """Get all registered drivers.
    """
    return _frozendict(_drivers)


def get_comment_statuses() -> dict:
    """Get valid comment statuses.
    """
    return {
        'published': _lang.t('pytsite.comments@status_published'),
        'waiting': _lang.t('pytsite.comments@status_waiting'),
        'spam': _lang.t('pytsite.comments@status_spam'),
        'deleted': _lang.t('pytsite.comments@status_deleted'),
    }


def get_comment_max_depth() -> int:
    """Get comment's max depth.
    """
    return _comment_max_depth


def get_comment_body_min_length() -> int:
    """Get comment's body minimum length.
    """
    return _comment_body_min_length


def get_comment_body_max_length() -> int:
    """Get comment's body maximum length.
    """
    return _comment_body_max_length


def get_driver(driver_name: str = None) -> _driver.Abstract:
    """Get driver instance.
    """
    if not driver_name:
        driver_name = _reg.get('comments.default_driver', _last_registered_driver_name)
        if not driver_name:
            raise _error.NoDriverRegistered('There is no comment drivers registered')

    if driver_name not in _drivers:
        raise _error.DriversNotRegistered("Driver '{}' is not registered".format(driver_name))

    return _drivers[driver_name]


def get_widget(widget_uid: str = 'comments', thread_id: str = None, driver_name: str = None) -> _widget.Abstract:
    """Get comments widget.
    """
    return get_driver(driver_name).get_widget(widget_uid, thread_id or _router.current_path(True))


def create_comment(thread_id: str, body: str, author: _auth.model.AbstractUser, status: str = 'published',
                   parent_uid: str = None, driver_name: str = None) -> _model.AbstractComment:
    """Create new comment.
    """
    # Check min length
    if len(body) < _comment_body_min_length:
        raise _error.CommentTooShort(_lang.t('pytsite.comments@error_body_too_short'))

    # Check max length
    if len(body) > _comment_body_max_length:
        raise _error.CommentTooLong(_lang.t('pytsite.comments@error_body_too_long'))

    # Check status
    if status not in get_comment_statuses():
        raise _error.InvalidCommentStatus("'{}' is not a valid comment's status.".format(status))

    # Load driver
    driver = get_driver(driver_name)

    # Create comment
    comment = driver.create_comment(thread_id, body, author, status, parent_uid)
    _events.fire('pytsite.comments.create_comment', comment=comment)

    # Send email notification about REPLY
    if _reg.get('comments.email.notify', True) and comment.is_reply:
        parent_comment = get_comment(comment.parent_uid)
        if comment.author != parent_comment.author:
            tpl_name = 'pytsite.comments@mail/{}/reply'.format(_lang.get_current())
            m_subject = _lang.t('pytsite.comments@mail_subject_new_reply')
            m_body = _tpl.render(tpl_name, {
                'reply': comment,
                'comment': get_comment(comment.parent_uid, driver_name)
            })
            m_from = '{} <{}>'.format(author.full_name, _mail.mail_from()[1])

            _mail.Message(parent_comment.author.email, m_subject, m_body, m_from).send()

    return comment


def get_comment(uid: str, driver_name: str = None) -> _model.AbstractComment:
    """Get single comment by UID.
    """
    return get_driver(driver_name).get_comment(uid)


def get_comments(thread_id: str, limit: int = 0, skip: int = 0, status: str = 'published', driver_name: str = None) \
        -> _Iterable[_model.AbstractComment]:
    """Get comments for a thread.
    """
    return get_driver(driver_name).get_comments(thread_id, limit, skip, status)


def delete_thread(thread_uid: str, driver_name: str = None):
    """Physically delete comments for particular thread.
    """
    get_driver(driver_name).delete_thread(thread_uid)


def get_comments_count(thread_uid: str, driver_name: str = None) -> int:
    """Get comments count for thread and driver.
    """
    c_key = '{}_{}'.format(thread_uid, driver_name)

    if _comments_count.has(c_key):
        return _comments_count.get(c_key)

    count = get_driver(driver_name).get_comments_count(thread_uid)
    _comments_count.put(c_key, count, 300)

    return count


def get_all_comments_count(thread_id: str):
    """Get comments count for particular thread, all drivers.
    """
    count = 0
    for driver_name in _drivers:
        count += get_comments_count(thread_id, driver_name)

    return count


def get_permissions(user: _auth.model.AbstractUser = None, driver_name: str = None) -> dict:
    """Get permissions definition for user.
    """
    if not user:
        user = _auth.get_current_user()

    return get_driver(driver_name).get_permissions(user)
