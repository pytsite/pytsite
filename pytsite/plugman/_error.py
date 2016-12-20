"""PytSite Plugin Manager Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ApiRequestError(Exception):
    pass


class InvalidLicense(Exception):
    pass


class UnknownPlugin(Exception):
    pass


class PluginNotInstalled(Exception):
    pass


class PluginAlreadyInstalled(Exception):
    pass


class PluginInstallationInProgress(Exception):
    pass


class PluginUninstallationInProgress(Exception):
    pass


class PluginInstallError(Exception):
    pass


class PackageInstallError(Exception):
    pass


class PluginUninstallError(Exception):
    pass


class PluginStartError(Exception):
    pass


class PluginAlreadyStarted(PluginStartError):
    pass
