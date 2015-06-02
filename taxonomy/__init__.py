"""Description.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang
from pytsite.admin import sidebar

lang.register_package(__name__)
sidebar.add_section('taxonomy', lang.t(__name__ + '@taxonomy'), 500)
