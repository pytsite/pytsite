"""PytSite Comments API.
"""
from typing import Dict as _Dict
from frozendict import frozendict as _frozendict
from pytsite import odm as _odm, router as _router, widget as _widget, auth as _auth, reg as _reg, lang as _lang, \
    cache as _cache
from . import _driver, _error, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_last_registered_driver_name = None  # type: str
_drivers = {}  # type: _Dict[str, _driver.Abstract]
_comments_count = _cache.create_pool('pytsite.comments.count')


def register_driver(driver: _driver.Abstract):
    """Registers a driver.
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
    """Returns all registered drivers.
    """
    return _frozendict(_drivers)


def get_comment_statuses() -> dict:
    """Get list of valid comment statuses.
    """
    return {
        'published': _lang.t('pytsite.comments@status_published'),
        'on_moderation': _lang.t('pytsite.comments@status_on_moderation'),
        'spam': _lang.t('pytsite.comments@status_spam'),
    }


def get_driver(driver_name: str = None) -> _driver.Abstract:
    """Get registered driver instance.
    """
    if not driver_name:
        driver_name = _reg.get('comments.default_driver', _last_registered_driver_name)

    if not _driver:
        raise _error.DriverNotRegistered('No comments driver registered.')

    if driver_name not in _drivers:
        raise _error.DriverNotRegistered("Driver '{}' is not registered".format(driver_name))

    return _drivers[driver_name]


def get_widget(widget_uid: str = 'comments', thread_id: str = None, driver: str = None) -> _widget.Base:
    """Get comments widget for particular driver.
    """
    return get_driver(driver).get_widget(widget_uid, thread_id or _router.current_url())


def create_comment(thread_id: str, body: str, author: _auth.model.AbstractUser, status: str = 'published',
                   driver_name: str = None) -> _model.CommentInterface:
    """Create new comment.
    """
    return get_driver(driver_name).create_comment(thread_id, body, author, status)


def get_comments_count(thread_id: str, driver_name: str = None) -> int:
    """Get comments count for particular thread and driver.
    """
    if _comments_count.has(thread_id):
        return _comments_count.get(thread_id)

    count = get_driver(driver_name).get_comments_count(thread_id)
    _comments_count.put(thread_id, count, 300)

    return count


def get_all_comments_count(thread_id: str):
    """Get comments count for particular thread, all drivers.
    """
    count = 0
    for driver_name in _drivers:
        count += get_comments_count(thread_id, driver_name)

    return count
