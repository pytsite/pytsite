"""PytSite pip Events Handlers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, lang as _lang, package_info as _package_info
from . import _api, _error


def update_stage_2():
    # Install/update pip packages
    _console.print_info(_lang.t('pytsite.pip@updating_packages'))
    for pkg_spec in _package_info.requires_packages('app'):
        try:
            _api.install(pkg_spec, _api.is_installed(pkg_spec))
        except _error.PackageInstallError as e:
            raise _console.error.CommandExecutionError(e)
