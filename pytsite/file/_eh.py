"""PytSite Image Package Event Handlers
"""
from pytsite import auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def setup():
    """`pytsite.setup` event handler.
    """
    # Allow ordinary users to create, modify and delete files
    user_role = _auth.get_role('user')
    user_role.permissions = list(user_role.permissions) + [
        'pytsite.odm_perm.create.file',
        'pytsite.odm_perm.view_own.file',
        'pytsite.odm_perm.modify_own.file',
        'pytsite.odm_perm.delete_own.file',
    ]
    user_role.save()
