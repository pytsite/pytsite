"""PytSite pip API
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import subprocess as _subprocess
from pytsite import semver as _semver
from . import _error

_installed_packages = {}


def get_installed_info(pkg_name: str) -> dict:
    """Get installed pip package info
    """
    cmd = ['pip', 'show', pkg_name]

    r = _subprocess.run(cmd, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE)

    if r.returncode != 0:
        raise _error.PackageNotInstalled(pkg_name)

    data = {}
    for r_str in r.stdout.decode('utf-8').split('\n'):
        r_str_split = r_str.split(':')
        k = r_str_split[0].strip().lower()
        if k:
            data[k] = ':'.join(r_str_split[1:]).strip()

    return data


def get_installed_version(pkg_name: str) -> str:
    """Get installed pip package version
    """
    return get_installed_info(pkg_name)['version']


def is_installed(pkg_spec: str) -> bool:
    """Check if the pip package installed
    """
    global _installed_packages

    if pkg_spec in _installed_packages:
        return _installed_packages[pkg_spec]

    pkg_name, version_req = _semver.parse_requirement_str(pkg_spec)

    try:
        r = _semver.check_conditions(get_installed_version(pkg_name), version_req)
        _installed_packages[pkg_spec] = r
        return r

    except _error.PackageNotInstalled:
        _installed_packages[pkg_spec] = False
        return False


def install(pkg_spec: str, upgrade: bool = False) -> str:
    """Install a pip package
    """
    cmd = ['pip', 'install']

    if upgrade:
        cmd.append('-U')

    cmd.append(pkg_spec)

    r = _subprocess.run(cmd, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE)

    if r.returncode != 0:
        raise _error.PackageInstallError(pkg_spec, r.stderr.decode('utf-8'))

    return r.stdout.decode('utf-8')


def uninstall(pkg_name: str) -> str:
    r = _subprocess.run(['pip', 'uninstall', '-y', pkg_name], stdout=_subprocess.PIPE, stderr=_subprocess.PIPE)

    if r.returncode != 0:
        raise _error.PackageUninstallError(pkg_name, r.stderr.decode('utf-8'))

    return r.stdout.decode('utf-8')
