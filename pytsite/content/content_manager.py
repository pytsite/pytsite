"""Content Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime
from pytsite.core import router
from pytsite.core.lang import t
from pytsite.core.odm import odm_manager
from pytsite.core.odm.finder import ODMFinder
from pytsite.admin import sidebar
from .models import ContentModel

__models = []


def register_model(model: str, cls: type, menu_weight: int=0, menu_icon: str='fa fa-file-text-o'):
    """Register content model.
    """
    if not issubclass(cls, ContentModel):
        raise TypeError('Subclass of ContentModel expected.')

    odm_manager.register_model(model, cls)
    __models.append(model)

    mock = odm_manager.dispense(model)

    menu_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    sidebar.add_menu('content', model, mock.t_plural(model), menu_url, menu_icon, weight=menu_weight, permissions=(
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


def find(model: str, status='published', check_publish_time=True) -> ODMFinder:
    """Get content entity.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as content model.".format(model))

    f = odm_manager.find(model)
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
        r.append((s, t('pytsite.content@status_' + s)))

    return r
