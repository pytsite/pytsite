"""PytSite Comments HTTP API.
"""
from pytsite import auth as _auth, lang as _lang, http as _http, events as _events
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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
    driver = inp.get('driver')

    thread_uid = inp.get('thread_uid')
    if not thread_uid:
        raise RuntimeError("'thread_uid' is not specified")

    limit = int(inp.get('limit', 100))
    if limit > 100:
        limit = 100

    skip = abs(int(inp.get('skip', 0)))
    comments = list(_api.get_driver(driver).get_comments(thread_uid, limit, skip))

    return {
        'permissions': _api.get_permissions(_auth.get_current_user(), driver),
        'remains': _api.get_comments_count(thread_uid, driver) - skip - len(comments),
        'max_depth': _api.get_comment_max_depth(),
        'items': [comment.as_jsonable() for comment in comments],
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
