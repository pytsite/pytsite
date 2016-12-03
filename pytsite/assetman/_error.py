"""PytSite Assetman Error
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PackageNotRegistered(Exception):
    pass


class PackageAlreadyRegistered(Exception):
    pass
