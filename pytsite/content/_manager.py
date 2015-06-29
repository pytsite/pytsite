"""Content Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime
from pytsite import admin as _admin, taxonomy as _taxonomy
from pytsite.core import odm as _odm, util as _util, router as _router, lang as _lang
from . import _model

__models = []


def register_model(model: str, cls, menu_title: str, menu_weight: int=0, menu_icon: str='fa fa-file-text-o'):
    """Register content model.
    """
    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, _model.Content):
        raise TypeError('Subclass of ContentModel expected.')

    _odm.register_model(model, cls)
    __models.append(model)

    menu_url = _router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    _admin.sidebar.add_menu('content', model, menu_title, menu_url, menu_icon, weight=menu_weight, permissions=(
        'pytsite.odm_ui.browse.' + model,
        'pytsite.odm_ui.browse_own.' + model,
    ))


def is_model_registered(model: str) -> bool:
    """Check if the content model is registered.
    """
    return model in __models


def get_registered_models() -> list:
    """Get registered content models.
    """
    return __models


def find(model: str, status='published', check_publish_time=True):
    """Get entity finder.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as content model.".format(model))

    f = _odm.find(model).sort([('publish_time', _odm.I_DESC)])
    if status:
        f.where('status', '=', status)
    if check_publish_time:
        f.where('publish_time', '<=', datetime.now())

    return f


def get_publish_statuses() -> list:
    """Get content publish statuses.
    """
    r = []
    for s in ('published', 'waiting', 'unpublished'):
        r.append((s, _lang.t('pytsite.content@status_' + s)))

    return r


def get_section(alias: str) -> _model.Section:
    return _taxonomy.find('section').where('alias', '=', alias).first()
