"""PytSite Comments HTTP API.
"""
from pytsite import auth as _auth, lang as _lang, http as _http, events as _events
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_settings(inp: dict) -> dict:
    """Get comments settings.
    """
    return {
        'body_min_length': _api.get_comment_body_min_length(),
        'body_max_length': _api.get_comment_body_max_length(),
        'max_depth': _api.get_comment_max_depth(),
        'statuses': _api.get_comment_statuses(),
        'permissions': _api.get_permissions(_auth.get_current_user(), inp.get('driver')),
    }


def post_comment(inp: dict) -> dict:
    """Create new comment.
    """
    driver = inp.get('driver')

    thread_uid = inp.get('thread_uid')
    if not thread_uid:
        raise RuntimeError("'thread_uid' is not specified")

    body = inp.get('body', '').strip()
    if not body:
        raise RuntimeError(_lang.t('pytsite.comments@comment_body_cannot_be_empty'))

    status = 'published'
    parent_uid = inp.get('parent_uid')
    comment = _api.create_comment(thread_uid, body, _auth.get_current_user(), status, parent_uid, driver)

    return comment.as_jsonable()


def get_comments(inp: dict) -> dict:
    """Get comments.
    """
    driver = inp.get('driver')

    thread_uid = inp.get('thread_uid')
    if not thread_uid:
        raise RuntimeError("'thread_uid' is not specified")

    limit = abs(int(inp.get('limit', 0)))
    skip = abs(int(inp.get('skip', 0)))
    comments = list(_api.get_driver(driver).get_comments(thread_uid, limit, skip))

    return {
        'items': [comment.as_jsonable() for comment in comments],
        'settings': get_settings(inp),
    }


def delete_comment(inp: dict) -> dict:
    """Delete comment.
    """
    driver = inp.get('driver')

    uid = inp.get('uid')
    if not uid:
        raise RuntimeError("'uid' argument is not specified.")

    try:
        _api.get_driver(driver).delete_comment(uid)
        return {'status': True}
    except _error.CommentNotExist as e:
        raise _http.error.NotFound(str(e))


def post_report(inp: dict) -> dict:
    """Report about comment.
    """
    uid = inp.get('uid')
    if not uid:
        raise RuntimeError("'uid' argument is not specified.")

    _events.fire('pytsite.comments.report_comment', uid=uid)

    return {'status': True}
