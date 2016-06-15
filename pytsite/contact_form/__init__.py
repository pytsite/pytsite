"""PytSite Contact Form.
"""
# Public API
from ._form import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, lang, tpl

    assetman.register_package(__name__)
    lang.register_package(__name__)
    tpl.register_package(__name__)


_init()
