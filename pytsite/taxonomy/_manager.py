"""Taxonomy Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


import re
from pytsite import admin
from pytsite.core import router, lang, util, odm
from ._model import Term

__models = []


def register_model(model: str, cls, menu_title: str, menu_weight: int=0, menu_icon: str='fa fa-tags'):
    """Register taxonomy model.

    :param cls: str|type
    """
    if is_model_registered(model):
        raise Exception("Model '{}' is already registered as taxonomy model.". format(model))

    if isinstance(cls, str):
        cls = util.get_class(cls)

    if not issubclass(cls, Term):
        raise TypeError('Subclass of AbstractTerm expected.')

    odm.manager.register_model(model, cls)
    __models.append(model)

    menu_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    admin.sidebar.add_menu('taxonomy', model, menu_title, menu_url, menu_icon, weight=menu_weight,
                     permissions=('pytsite.odm_ui.browse.' + model,))


def is_model_registered(model: str) -> bool:
    """Check if the model is registered as taxonomy model.
    """
    return model in __models


def dispense(model: str, title: str):
    """Create new term or dispense existing.
    """
    title = title.strip()
    term = find(model).where('title', 'regex_i', '^' + title + '$').first()
    if not term:
        term = odm.manager.dispense(model).f_set('title', title)

    return term


def find(model: str) -> odm.finder.ODMFinder:
    """Get finder for the taxonomy model.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as taxonomy model.". format(model))

    return odm.manager.find(model).where('language', '=', lang.get_current_lang()).sort([('weight', odm.I_DESC)])


def sanitize_alias_string(model: str, string: str) -> str:
    """Sanitize a path string.
    """
    string = util.transform_str_1(string)

    itr = 0
    while True:
        if not find(model).where('alias', '=', string).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub(r'-\d+$', '-' + str(itr), string)
