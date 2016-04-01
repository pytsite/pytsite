"""pytsite.browser API Functions.
"""
from typing import Callable as _Callable
from pytsite import assetman as _assetman, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__libraries = {}


def register(lib: str, callback: _Callable):
    """Register a library.
    """
    if lib in __libraries:
        raise KeyError("Browser library '{}' is already registered.".format(lib))

    __libraries[lib] = callback


def get_assets(lib: str, **kwargs) -> list:
    """Get assets of the library.
    """
    if lib in __libraries:
        return __libraries[lib](**kwargs)
    else:
        raise ValueError("Unknown browser library: '{}'.".format(lib))


def include(lib: str, permanent=False, path_prefix: str = None, **kwargs):
    """Include the library.
    """
    for asset in get_assets(lib, **kwargs):
        _assetman.add(asset, permanent, path_prefix=path_prefix)
