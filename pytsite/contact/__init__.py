"""PytSite Contact Form.
"""
from pytsite import assetman as _assetman, lang as _lang, tpl as _tpl
from ._form import Contact as ContactForm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_assetman.register_package(__name__)
_lang.register_package(__name__)
_tpl.register_package(__name__)

_assetman.add('pytsite.contact@js/common.js', forever=True)
