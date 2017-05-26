"""PytSite Plugin Manager Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ApiRequestError(Exception):
    pass


class UnknownPlugin(Exception):
    pass


class PluginNotInstalled(Exception):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is not installed".format(self._name)


class PluginAlreadyInstalled(Exception):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is already installed".format(self._name)



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


class PluginAlreadyStarted(Exception):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is already started".format(self._name)


class PluginNotStarted(Exception):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is not started".format(self._name)
