"""Event Handlers.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.lang import t
from pytsite.core.validation import Validator, EmailRule, NotEmptyRule
from . import auth_manager


def app_setup():
    """'app.setup' Event Handler.
    """

    # Creating roles
    admin_role = ('admin', 'pytsite.auth@admin_role_description')
    user_role = ('user', 'pytsite.auth@user_role_description')
    for role in admin_role, user_role:
        if not auth_manager.get_role(name=role[0]):
            role_entity = auth_manager.create_role(role[0], role[1])
            if role_entity.f_get('name') == 'admin':
                role_entity.f_add('permissions', 'admin')
            role_entity.save()
            print(t('pytsite.auth@role_has_been_created', {'name': role_entity.f_get('name')}))

    # Creating administrator
    email = input(t('pytsite.auth@enter_admin_email') + ': ')
    v = Validator()
    v.add_rule('email', NotEmptyRule()).add_rule('email', EmailRule()).set_value('email', email)
    if not v.validate():
        raise Exception(v.messages)
    admin_user = auth_manager.create_user(email)
    admin_user.f_set('fullName', t('pytsite.auth@administrator'))
    admin_user.f_add('roles', auth_manager.get_role('admin'))
    admin_user.save()
    print(t('pytsite.auth@user_has_been_created', {'login': admin_user.f_get('login')}))
