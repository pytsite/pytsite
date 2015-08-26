"""PytSite Setup Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path as _path
from pytsite import reg as _reg

def is_setup_completed() -> bool:
    return _path.exists(_reg.get('paths.setup.lock'))
