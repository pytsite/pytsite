"""PytSite Tpl Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import jinja2 as _jinja


class TemplateNotFound(_jinja.TemplateNotFound):
    pass
