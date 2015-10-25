"""Pytsite Hreflang Functions.
"""
from pytsite import lang as _lang, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__links = {}


def add(lang: str, href: str):
    __links[lang] = href


def get(lang: str) -> str:
    return __links.get(lang)


def get_all() -> dict:
    return __links


def reset() -> str:
    global __links
    __links = {}

    if _router.is_base_url():
        for lng in _lang.langs(False):
            add(lng, _router.base_url(lng))
