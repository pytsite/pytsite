"""Taxonomy Functions.
"""
import re
from pytsite import admin as _admin, router as _router, lang as _lang, util as _util, odm as _odm
from ._model import Term

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

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

    menu_url = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model})
    _admin.sidebar.add_menu('taxonomy', model, menu_title, menu_url, menu_icon, weight=menu_weight,
                            permissions=('pytsite.odm_ui.browse.' + model,))


def is_model_registered(model: str) -> bool:
    """Check if the model is registered as taxonomy model.
    """
    return model in __models


def find(model: str, language: str=None):
    """Get finder for the taxonomy model.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as taxonomy model.". format(model))

    if not language:
        language = _lang.get_current()

    return _odm.find(model).where('language', '=', language).sort([('weight', _odm.I_DESC)])


def dispense(model: str, title: str, alias: str=None, language: str=None) -> Term:
    """Create new term or dispense existing.
    """
    if not is_model_registered(model):
        raise Exception("Model '{}' is not registered as taxonomy model.". format(model))

    if not language:
        language = _lang.get_current()

    title = title.strip()

    if not alias:
        alias = _util.transform_str_2(title)

    # Trying to find term by title
    term = find(model, language).where('title', 'regex_i', '^' + title + '$').first()

    # If term is not found, trying to find it by alias
    if not term:
        term = find(model, language).where('alias', '=', alias).first()

    # If term is not found, create it
    if not term:
        term = _odm.dispense(model)
        term.f_set('title', title).f_set('language', language)
        if alias:
            term.f_set('alias', alias)

    return term


def sanitize_alias_string(model: str, string: str) -> str:
    """Sanitize a path string.
    """
    string = _util.transform_str_2(string)

    itr = 0
    while True:
        if not find(model).where('alias', '=', string).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub(r'-\d+$', '-' + str(itr), string)
