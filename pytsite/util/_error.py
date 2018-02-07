"""PytSite Util Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class PytSiteVersionNotInstalled(Error):
    def __init__(self, version: str):
        super().__init__()

        self._version = version

    def __str__(self) -> str:
        return "PytSite{} is not installed".format(self._version)
