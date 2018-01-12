"""PytSite Util Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class PipPackageInstallError(Error):
    def __init__(self, req: str, err_msg: str):
        super().__init__()

        self._req_str = req
        self._err_msg = err_msg

    def __str__(self) -> str:
        return "Error while installing pip package '{}': {}".format(self._req_str, self._err_msg)


class PytSiteVersionNotInstalled(Error):
    def __init__(self, version: str):
        super().__init__()

        self._version = version

    def __str__(self) -> str:
        return "PytSite{} is not installed".format(self._version)


class PipPackageNotInstalled(Error):
    def __init__(self, pkg_spec: str):
        super().__init__()

        self._pkg_spec = pkg_spec

    def __str__(self) -> str:
        return "Pip package {} is not installed".format(self._pkg_spec)


class PluginNotInstalled(Error):
    def __init__(self, plugin_spec: str):
        super().__init__()

        self._plugin_spec = plugin_spec

    def __str__(self) -> str:
        return "Plugin {} is not installed".format(self._plugin_spec)
