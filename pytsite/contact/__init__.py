"""PytSite Contact Form.
"""
# Public API
from ._form import Contact as ContactForm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, lang, tpl, browser

    assetman.register_package(__name__)
    assetman.add('pytsite.contact@js/common.js', forever=True)
    lang.register_package(__name__)
    tpl.register_package(__name__)
    browser.register_ep('pytsite.contact.ep.submit')


__init()
