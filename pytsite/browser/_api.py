"""pytsite.browser API Functions.
"""
from typing import Callable as _Callable
from pytsite import assetman as _assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_libraries = {}


def register(lib: str, callback: _Callable):
    """Register a library.
    """
    if lib in _libraries:
        raise KeyError("Browser library '{}' is already registered.".format(lib))

    _libraries[lib] = callback


def get_assets(lib: str, **kwargs) -> list:
    """Get assets of the library.
    """
    if lib in _libraries:
        return _libraries[lib](**kwargs)
    else:
        raise ValueError("Unknown browser library: '{}'.".format(lib))


def include(lib: str, permanent=False, path_prefix: str = None, **kwargs):
    """Include the library.
    """
    for asset in get_assets(lib, **kwargs):
        location = asset

        if isinstance(asset, (list, tuple)):
            collection = asset[1]
            location = asset[0]
        else:
            collection = _assetman.detect_collection(location)

        _assetman.add(location, permanent, collection, path_prefix=path_prefix)
