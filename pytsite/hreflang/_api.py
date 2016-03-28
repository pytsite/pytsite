"""Pytsite Hreflang Functions.
"""
from pytsite import lang as _lang, router as _router, threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_links = {}


def add(lang: str, href: str):
    tid = _threading.get_id()
    if tid not in _links:
        _links[tid] = {}

    _links[tid][lang] = href


def get(lang: str) -> str:
    tid = _threading.get_id()
    if tid not in _links:
        _links[tid] = {}

    return _links[tid].get(lang)


def get_all() -> dict:
    tid = _threading.get_id()
    if tid not in _links:
        _links[tid] = {}

    return _links[tid]


def reset() -> str:
    _links[_threading.get_id()] = {}

    if _router.is_base_url():
        for lng in _lang.langs(False):
            add(lng, _router.base_url(lng))
