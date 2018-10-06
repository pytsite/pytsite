"""PytSite pip Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import reg as _reg, console as _console, lang as _lang, package_info as _package_info
from . import _api, _error


def update_stage_2():
    # Install/update pip packages
    _console.print_info(_lang.t('pytsite.pip@updating_packages'))
    for pkg_name, pkg_ver in _package_info.requires_packages('app').items():
        try:
            _api.install(pkg_name, pkg_ver, True, _reg.get('debug'))
        except _error.PackageInstallError as e:
            raise _console.error.CommandExecutionError(e)
