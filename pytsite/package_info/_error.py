"""PytSite Package Utilities Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class InvalidRequirementString(Exception):
    pass


class MissingRequiredPackage(Exception):
    def __init__(self, package_name: str):
        super().__init__()

        self._package_name = package_name

    def __str__(self) -> str:
        return "Package {} is not installed".format(self._package_name)


class MissingRequiredVersion(Exception):
    def __init__(self, package_name: str, required_package_name: str, condition: str, installed_version: str):
        super().__init__()

        self._package_name = package_name
        self._required_package_name = required_package_name
        self._condition = condition
        self._installed_version = installed_version

    def __str__(self):
        return "'{}' requires {}{}, but {}-{} is currently installed". \
            format(self._package_name, self._required_package_name, self._condition,
                   self._required_package_name, self._installed_version)
