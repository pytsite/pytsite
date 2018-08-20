"""
"""

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class PackageInstallError(Error):
    def __init__(self, req: str, err_msg: str):
        super().__init__()

        self._req_str = req
        self._err_msg = err_msg

    def __str__(self) -> str:
        return "Error while installing pip package '{}': {}".format(self._req_str, self._err_msg)


class PackageUninstallError(Error):
    def __init__(self, pkg_name: str, err_msg: str):
        super().__init__()

        self._pkg_name = pkg_name
        self._err_msg = err_msg

    def __str__(self) -> str:
        return "Error while uninstalling pip package '{}': {}".format(self._pkg_name, self._err_msg)


class PackageNotInstalled(Error):
    def __init__(self, pkg_spec: str):
        super().__init__()

        self._pkg_spec = pkg_spec

    def __str__(self) -> str:
        return "Pip package {} is not installed".format(self._pkg_spec)
