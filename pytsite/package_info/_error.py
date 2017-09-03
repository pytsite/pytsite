"""PytSite Package Utilities Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PackageNotFound(Exception):
    pass


class MissingRequiredPipPackage(Exception):
    pass


class MissingRequiredPipPackageVersion(Exception):
    pass
