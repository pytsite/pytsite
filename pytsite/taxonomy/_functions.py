"""Taxonomy Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from pytsite import admin as _admin
from pytsite.core import router as _router, lang as _lang, util as _util, odm as _odm
from ._model import Term

__models = []


def register_model(model: str, cls, menu_title: str, menu_weight: int=0, menu_icon: str='fa fa-tags'):
    """Register taxonomy model.
    :param cls: str|type
    """
    if is_model_registered(model):
        raise Exception("Model '{}' is already registered as taxonomy model.". format(model))

    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, Term):
        raise TypeError('Subclass of AbstractTerm expected.')

    _odm.register_model(model, cls)
    __models.append(model)

    menu_url = _router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    _admin.sidebar.add_menu('taxonomy', model, menu_title, menu_url, menu_icon, weight=menu_weight,
                            permissions=('pytsite.odm_ui.browse.' + model,))


def is_model_registered(model: str) -> bool:
    """Check if the model is registered as taxonomy model.
    """
    return model in __models


def dispense(model: str, title: str, alias: str=None):
    """Create new term or dispense existing.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as taxonomy model.". format(model))

    title = title.strip()
    term = find(model).where('title', 'regex_i', '^' + title + '$').first()
    if not term and alias:
        term = find(model).where('alias', '=', alias).first()

    if not term:
        term = _odm.dispense(model).f_set('title', title)
        if alias:
            term.f_set('alias', alias)

    return term


def find(model: str, language: str=None):
    """Get finder for the taxonomy model.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as taxonomy model.". format(model))

    if not language:
        language = _lang.get_current_lang()

    return _odm.find(model).where('language', '=', language).sort([('weight', _odm.I_DESC)])


def sanitize_alias_string(model: str, string: str) -> str:
    """Sanitize a path string.
    """
    string = _util.transform_str_1(string)

    itr = 0
    while True:
        if not find(model).where('alias', '=', string).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub(r'-\d+$', '-' + str(itr), string)
