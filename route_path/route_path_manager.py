"""Route Paths Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from pytsite.core.lang import transliterate, get_current_lang
from pytsite.core.odm import odm_manager
from .models import RoutePathModel


def create_path(alias: str, target: str=None) -> RoutePathModel:
    alias = sanitize_path_string(alias)
    entity = odm_manager.dispense('route_path')
    entity.f_set('alias', alias)
    entity.f_set('target', target)
    entity.f_set('language', get_current_lang())
    return entity


def sanitize_path_string(string: str) -> str:
    mapping = {
        '!': '', '@': '', '#': '', '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '_': '', '-': '',
        '=': '', '+': '', '"': '', "'": '', '{': '', '}': '', '[': '', ']': '', '`': '', '~': '', '|': '', '\\': '',
        '?': '', '.': '', ',': '', '<': '', '>': '', '«': '', '»': '', '№': '', ':': '', ';': '',
    }

    for k, v in mapping.items():
        string = string.replace(k, v)

    string = transliterate(string)
    string = re.sub(r'/{2,}', '-', string)
    string = re.sub(r'[^a-zA-Z0-9/]', '-', string)
    string = re.sub(r'-{2,}', '-', string)

    if not string.startswith('/'):
        string = '/' + string

    string = re.sub(r'^/-', '/', string)

    itr = 0
    while True:
        if not odm_manager.find('route_path').where('alias', '=', string).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub(r'-\d+$', '-' + str(itr), string)
