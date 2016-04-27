"""PytSite Comments API.
"""
from typing import Dict as _Dict
from datetime import datetime as _datetime
from frozendict import frozendict as _frozendict
from pytsite import odm as _odm, router as _router, widget as _widget
from . import _driver, _error, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_drivers = {}  # type: _Dict[str, _driver.Driver]


def register_driver(driver: _driver.Driver):
    """Registers a driver.
    """
    global _drivers

    if not isinstance(driver, _driver.Driver):
        raise TypeError("Instance of 'pytsite.comments.driver.Abstract' expected.")

    driver_name = driver.get_name()

    if driver_name in _drivers:
        raise _error.DriverAlreadyRegistered("Driver '{}' is already registered".format(driver_name))

    _drivers[driver_name] = driver


def get_drivers() -> _frozendict:
    """Returns all registered drivers.
    """
    return _frozendict(_drivers)


def get_driver(driver_name: str) -> _driver.Driver:
    """Get registered driver instance.
    """
    if driver_name not in _drivers:
        raise _error.DriverNotRegistered("Driver '{}' is not registered".format(driver_name))

    return _drivers[driver_name]


def get_widget(driver_name: str, widget_uid: str= 'comments', thread_id: str=None) -> _widget.Base:
    """Get comments widget for particular driver.
    """
    return get_driver(driver_name).get_widget(widget_uid, thread_id or _router.current_url())


def get_comments_count(driver_name: str, thread_id: str) -> int:
    """Get comments count for particular thread and driver.
    """
    driver = get_driver(driver_name)

    f = _odm.find('comments_count').where('driver', '=', driver.get_name()).where('thread_id', '=', thread_id)
    entity = f.first()  # type: _model.CommentsCount

    if entity:
        time_diff = _datetime.now() - entity.modified
        if time_diff.seconds <= 1800:  # 30 min
            return entity.count
    else:
        entity = _odm.dispense('comments_count')
        entity.f_set('driver', driver.get_name())
        entity.f_set('thread_id', thread_id)
        entity.save()

    comments_count = driver.get_comments_count(thread_id)
    entity.f_set('count', comments_count).save()

    return comments_count


def get_all_comments_count(thread_id: str):
    """Get comments count for particular thread, all drivers.
    """
    count = 0
    for driver_name in _drivers:
        count += get_comments_count(driver_name, thread_id)

    return count
