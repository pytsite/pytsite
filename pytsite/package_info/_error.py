"""PytSite Package Info Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class PackageNotFound(Error):
    pass


class RequiredPytSiteVersionNotInstalled(Error):
    pass


class RequiredPipPackageNotInstalled(Error):
    def __init__(self, pkg_spec: str):
        super().__init__()

        self._pkg_spec = pkg_spec

    def __str__(self) -> str:
        return "Required pip package '{}' is not installed. Try to run console pip:install '{}'". \
            format(self._pkg_spec, self._pkg_spec)


class RequiredPluginNotInstalled(Error):
    def __init__(self, plugin_spec: str):
        super().__init__()

        self._plugin_spec = plugin_spec

    def __str__(self) -> str:
        return "Required plugin '{}' is not installed. Try to run console plugman:install '{}'". \
            format(self._plugin_spec, self._plugin_spec)
