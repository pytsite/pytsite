"""PytSite Plugin Manager Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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


class PluginStartError(Exception):
    pass


class PluginNotLoaded(Exception):
    pass

class PluginReloadError(Exception):
    pass
