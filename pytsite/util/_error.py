"""PytSite Util Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PipPackageInstallError(Exception):
    def __init__(self, req: str, err_msg: str):
        super().__init__()

        self._req_str = req
        self._err_msg = err_msg

    def __str__(self) -> str:
        return "Error while installing pip package '{}': {}".format(self._req_str, self._err_msg)


class PipPackageNotInstalled(Exception):
    def __init__(self, pkg_name: str):
        super().__init__()

        self._pkg_name = pkg_name

    def __str__(self) -> str:
        return "Pip package '{}' is not installed".format(self._pkg_name)
