"""PytSite Comments HTTP API.
"""
from pytsite import auth as _auth, lang as _lang, http as _http, events as _events
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_settings(**kwargs) -> dict:
    """Get comments settings.
    """
    return {
        'body_min_length': _api.get_comment_body_min_length(),
        'body_max_length': _api.get_comment_body_max_length(),
        'max_depth': _api.get_comment_max_depth(),
        'statuses': _api.get_comment_statuses(),
        'permissions': _api.get_permissions(_auth.get_current_user(), kwargs.get('driver')),
    }


def post_comment(**kwargs) -> dict:
    """Create new comment.
    """
    driver = kwargs.get('driver')

    thread_uid = kwargs.get('thread_uid')
    if not thread_uid:
        raise RuntimeError("'thread_uid' is not specified")

    body = kwargs.get('body', '').strip()
    if not body:
        raise RuntimeError(_lang.t('pytsite.comments@comment_body_cannot_be_empty'))

    status = 'published'
    parent_uid = kwargs.get('parent_uid')
    comment = _api.create_comment(thread_uid, body, _auth.get_current_user(), status, parent_uid, driver)

    return comment.as_jsonable()


def get_comments(**kwargs) -> dict:
    """Get comments.
    """
    driver = kwargs.get('driver')

    thread_uid = kwargs.get('thread_uid')
    if not thread_uid:
        raise RuntimeError("'thread_uid' is not specified")

    limit = abs(int(kwargs.get('limit', 0)))
    skip = abs(int(kwargs.get('skip', 0)))
    comments = list(_api.get_driver(driver).get_comments(thread_uid, limit, skip))

    return {
        'items': [comment.as_jsonable() for comment in comments],
        'settings': get_settings(**kwargs),
    }


def delete_comment(**kwargs) -> dict:
    """Delete comment.
    """
    driver = kwargs.get('driver')

    uid = kwargs.get('uid')
    if not uid:
        raise RuntimeError("'uid' argument is not specified.")

    try:
        _api.get_driver(driver).delete_comment(uid)
        return {'status': True}
    except _error.CommentNotExist as e:
        raise _http.error.NotFound(str(e))


def post_report(**kwargs) -> dict:
    """Report about comment.
    """
    uid = kwargs.get('uid')
    if not uid:
        raise RuntimeError("'uid' argument is not specified.")

    _events.fire('pytsite.comments.report_comment', uid=uid)

    return {'status': True}
