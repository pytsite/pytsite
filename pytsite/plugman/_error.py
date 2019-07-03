"""PytSite Plugin Manager Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import semver


class Error(Exception):
    pass


class PluginsApiError(Error):
    def __init__(self, request_url: str, error_content: str):
        self._request_url = request_url
        self._error_content = error_content

    @property
    def request_url(self) -> str:
        return self._request_url

    @property
    def error_content(self) -> str:
        return self._error_content

    def __str__(self) -> str:
        return "Error while requesting plugin API URL '{}': {}".format(self._request_url, self._error_content)


class UnknownPlugin(Error):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is unknown".format(self._name)


class UnknownPluginVersion(Error):
    def __init__(self, plugin_name: str, v_range: semver.VersionRange):
        self._name = plugin_name
        self._v_range = v_range

    def __str__(self) -> str:
        return "Plugin '{}' has no version(s) {}".format(self._name, self._v_range)


class PluginPackageNotFound(Error):
    """Plugin is not found on the filesystem
    """

    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Package of the plugin '{}' is not found on the filesystem".format(self._name)


class PluginNotInstalled(Error):
    """Plugin is found on the filesystem, but is not completely installed
    """

    def __init__(self, plugin_spec: str, required_by: str = None):
        self._spec = plugin_spec
        self._required_by = required_by

    def __str__(self) -> str:
        if self._required_by:
            return "Plugin '{}', required by '{}', is not installed".format(self._spec, self._required_by)
        else:
            return "Plugin '{}' is not installed".format(self._spec)


class PluginAlreadyInstalled(Error):
    def __init__(self, name: str, version: str):
        self._name = name
        self._version = version

    def __str__(self) -> str:
        return "Plugin '{}-{}' is already installed".format(self._name, self._version)


class PluginInstallationInProgress(Error):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is not completely installed yet".format(self._name)


class PluginUninstallationInProgress(Error):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Uninstallation of the plugin '{}' is already started".format(self._name)


class PluginInstallError(Error):
    pass


class PluginUninstallError(Error):
    pass


class PluginLoadError(Error):
    pass


class CircularDependencyError(Error):
    def __init__(self, plugin_name: str, required_by: str = None):
        self._name = plugin_name
        self._required_by = required_by

    def __str__(self) -> str:
        if self._required_by:
            return "Plugin '{}' is already loading as a requirement of '{}'".format(self._name, self._required_by)
        else:
            return "Plugin '{}' is already loading".format(self._name)


class PluginNotLoaded(Error):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is not loaded".format(self._name)


class PluginDependencyError(Error):
    pass
