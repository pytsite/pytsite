"""PytSite pip Support Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import reg, console, lang, package_info
from . import _api, _error


def update_stage_2():
    # Install/update pip packages
    console.print_info(lang.t('pytsite.pip@updating_packages'))
    for pkg_name, pkg_ver in package_info.requires_packages('app').items():
        try:
            _api.install(pkg_name, pkg_ver, True, reg.get('debug'))
        except _error.PackageInstallError as e:
            raise console.error.CommandExecutionError(e)
