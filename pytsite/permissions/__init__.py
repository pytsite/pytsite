"""PytSite Permission Package.
"""
from ._api import define_permission, define_group, get_permission, is_permission_group_defined, \
    get_permission_groups, get_permissions, is_permission_defined


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    define_group('app', 'app@app_name')


_init()
