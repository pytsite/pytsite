"""Poster Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import threading
from datetime import datetime, timedelta
from pytsite import content as _content
from pytsite.core import odm as _odm, lang as _lang, logger as _logger
from . import _driver

__drivers = {}


def register_driver(name: str, title: str, driver_cls: type):
    """Register export driver.
    """
    if name in __drivers:
        raise KeyError("Driver with name '{}' already registered.")

    if not issubclass(driver_cls, _driver.Abstract):
        raise ValueError("Invalid driver's class.")

    __drivers[name] = (title, driver_cls)


def load_driver(name: str, **kwargs) -> _driver.Abstract:
    """Instantiate driver.
    """
    return get_driver_info(name)[1](**kwargs)


def get_driver_info(name: str) -> tuple:
    if name not in __drivers:
        raise KeyError("Driver with name '{}' is not registered.")

    return __drivers[name]


def get_drivers() -> dict:
    """Get registered drivers.
    """
    return __drivers


def get_driver_title(name) -> str:
    return _lang.t(get_driver_info(name)[0])


def cron_15m_event_handler():
    """'odm.save' event handler.
    """
    for exporter in _odm.find('content_export').get():
        content_f = _content.find(exporter.content_model)
        content_f.where('publish_time', '>=', datetime.now() - timedelta(1))
        content_f.where('options.content_export', 'nin', [str(exporter.id)])
        content_f.sort([('publish_time', _odm.I_ASC)])

        # Filter by content owner
        if not exporter.process_all_authors:
            content_f.where('author', '=', exporter.owner)

        for entity in content_f.get():
            _logger.info("{}. Entity '{}', title='{}'. Exporter '{}', title='{}'" \
                         .format(__name__, entity.model, entity.title, exporter.driver, exporter.driver_opts['title']))
            driver = load_driver(exporter.driver, **exporter.driver_opts)
            driver.export(entity=entity, exporter=exporter)
