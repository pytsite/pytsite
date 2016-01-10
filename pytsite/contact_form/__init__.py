"""PytSite Contact Form.
"""
# Public API
from ._form import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, lang, tpl, browser

    assetman.register_package(__name__)
    lang.register_package(__name__)
    tpl.register_package(__name__)
    browser.register_ep('pytsite.contact_form.ep.submit')


__init()
