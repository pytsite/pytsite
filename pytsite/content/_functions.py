"""Content Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime
from pytsite import admin as _admin, taxonomy as _taxonomy, auth as _auth
from pytsite.core import odm as _odm, util as _util, router as _router, lang as _lang
from . import _model

__models = {}


def register_model(model: str, cls, title: str, menu_weight: int=0, icon: str='fa fa-file-text-o', replace=False):
    """Register content model.
    """
    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, _model.Content):
        raise TypeError('Subclass of content model expected.')

    if not replace and is_model_registered(model):
        raise KeyError("Model '{}' is already registered.".format(model))

    _odm.register_model(model, cls, replace)
    __models[model] = (cls, title)

    mock = _odm.dispense(model)
    perm_name = 'pytsite.content.bypass_moderation.' + model
    perm_description = mock.package_name() + '@content_permission_bypass_moderation_' + model
    _auth.define_permission(perm_name, perm_description, mock.package_name())

    menu_url = _router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    _admin.sidebar.add_menu('content', model, title, menu_url, icon, weight=menu_weight, permissions=(
        'pytsite.odm_ui.browse.' + model,
        'pytsite.odm_ui.browse_own.' + model,
    ), replace=replace)


def is_model_registered(model: str) -> bool:
    """Check if the content model is registered.
    """
    return model in __models


def get_models() -> dict:
    """Get registered content models.
    """
    return __models


def get_model(model: str) -> tuple:
    """Get model information.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    return __models[model]


def create(model: str) -> _model.Content:
    """Create content entity.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    return _odm.dispense(model)


def find(model: str, status='published', check_publish_time=True):
    """Get content entities finder.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    f = _odm.find(model).sort([('publish_time', _odm.I_DESC)])
    if status:
        f.where('status', '=', status)
    if check_publish_time:
        f.where('publish_time', '<=', _datetime.now())

    return f


def get_publish_statuses() -> list:
    """Get allowed content publication statuses.
    """
    r = []
    for s in ('published', 'waiting', 'unpublished'):
        r.append((s, _lang.t('content@status_' + s)))

    return r

def get_section(alias: str) -> _model.Section:
    return _taxonomy.find('section').where('alias', '=', alias).first()