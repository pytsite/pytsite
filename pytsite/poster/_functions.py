"""Poster Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import oauth as _oauth, content as _content
from pytsite.core import odm as _odm, lang as _lang
from . import _driver

__drivers = {}


def register_driver(name: str, title: str, driver_cls: type):
    """Register oAuth driver.
    """
    if name in __drivers:
        raise KeyError("Driver with name '{}' already registered.")

    if not issubclass(driver_cls, _driver.Abstract):
        raise ValueError("Invalid driver's class.")

    __drivers[name] = (title, driver_cls)


def load_driver(name: str, **kwargs) -> _driver.Abstract:
    """Instantiate driver.
    """
    if name not in __drivers:
        raise KeyError("Driver with name '{}' is not registered.")

    return __drivers[name][1](**kwargs)


def get_drivers() -> dict:
    """Get registered drivers.
    """
    return __drivers


def content_save_event_handler(entity: _content.model.Content):
    """'odm.save' event handler.
    """
    f = _odm.find('poster')\
        .where('content_model', '=', entity.model)\
        .where('owner', '=', entity.f_get('author'))

    for poster in f.get():
        oauth_acc = poster.f_get('oauth_account')
        """:type: pytsite.oauth._model.Account"""

        tags = []
        for tag in entity.tags:
            tags.append(tag.title)

        oauth_acc.status_update(
            title=entity.title,
            description=entity.description,
            body=entity.body,
            tags=tags,
            media=entity.images,
            url=entity.url
        )

def oauth_pre_delete_account_event_handler(entity: _oauth.model.Account):
    """'odm.entity.pre_delete.oauth_account' event handler.
    """
    if _odm.find('poster').where('oauth_account', '=', entity).first():
        raise _odm.error.ForbidEntityDelete(
            _lang.t('pytsite.poster@cannot_delete_oauth_account_because_poster_exists'))