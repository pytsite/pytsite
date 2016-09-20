"""PytSite Permissions API.
"""
from frozendict import frozendict as _frozendict
from pytsite import events as _events
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_groups = {}
_permissions = []


def is_permission_group_defined(name: str) -> bool:
    """Get permission group spec.
    """
    return name in _groups


def define_group(name: str, description: str):
    """Define permission group.
    """
    if name in _groups:
        raise _error.PermissionGroupAlreadyDefined("Permission group '{}' is already defined.".format(name))

    _groups[name] = description


def get_permission_groups() -> _frozendict:
    """Get all defined permission groups.
    """
    return _frozendict(_groups)


def get_permissions(group: str = None) -> list:
    """Get defined permissions spec.
    """
    r = []
    for perm in _permissions:
        if group and perm[2] != group:
            continue
        r.append(perm)

    return r


def get_permission(name: str) -> tuple:
    """Get single permission spec.
    """
    for perm in _permissions:
        if perm[0] == name:
            return perm

    raise _error.PermissionNotDefined("Permission '{}' is not defined.".format(name))


def is_permission_defined(name: str) -> bool:
    """Check if the permission is defined.
    """
    try:
        get_permission(name)
        return True
    except _error.PermissionNotDefined:
        return False


def define_permission(name: str, description: str, group: str):
    """Define a permission.
    """
    if group not in _groups:
        raise _error.PermissionGroupNotDefined("Permission group '{}' is not defined.".format(group))

    try:
        get_permission(name)
        raise _error.PermissionAlreadyDefined("Permission '{}' is already defined.".format(name))
    except _error.PermissionNotDefined:
        _permissions.append((name, description, group))
        _events.fire('pytsite.permission.define', name=name)
