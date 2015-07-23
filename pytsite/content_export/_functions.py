"""Poster Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import threading
from datetime import datetime
from pytsite import content as _content
from pytsite.core import odm as _odm, lang as _lang
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


def content_save_event_handler(entity: _content.model.Content):
    """'odm.save' event handler.
    """
    if entity.status != 'published' or entity.publish_time > datetime.now():
        return

    f = _odm.find('content_export').where('content_model', '=', entity.model).where('owner', '=', entity.author)
    for exporter in f.get():
        driver = load_driver(exporter.driver, **exporter.driver_opts)
        threading.Thread(target=driver.export, kwargs={'entity': entity, 'exporter': exporter}).start()
