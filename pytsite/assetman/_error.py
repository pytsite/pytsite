"""PytSite Assetman Error
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PackageNotRegistered(Exception):
    def __init__(self, package_name: str):
        self._package_name = package_name

    def __str__(self):
        return "Assetman package '{}' is not registered".format(self._package_name)


class PackageAlreadyRegistered(Exception):
    def __init__(self, package_name: str):
        self._package_name = package_name

    def __str__(self):
        return "Assetman package '{}' is already registered".format(self._package_name)


class LibraryAlreadyRegistered(Exception):
    def __init__(self, package_name: str):
        self._package_name = package_name

    def __str__(self):
        return "Assetman library '{}' is already registered".format(self._package_name)


class PackageAliasAlreadyUsed(Exception):
    def __init__(self, package_alias: str):
        self._package_alias = package_alias

    def __str__(self):
        return "Assetman package alias '{}' is already used".format(self._package_alias)
