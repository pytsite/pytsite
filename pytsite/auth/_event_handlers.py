"""Event Handlers.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import console, lang, validation
from . import _manager


def app_setup():
    """'app.setup' Event Handler.
    """
    # Creating roles
    admin_role = ('admin', 'pytsite.auth@admin_role_description')
    user_role = ('user', 'pytsite.auth@user_role_description')
    for role in admin_role, user_role:
        if not _manager.get_role(name=role[0]):
            role_entity = _manager.create_role(role[0], role[1])
            if role_entity.f_get('name') == 'admin':
                role_entity.f_add('permissions', 'admin')
            role_entity.save()
            console.print_success(lang.t('pytsite.auth@role_has_been_created', {'name': role_entity.f_get('name')}))

    # Creating administrator
    try:
        email = input(lang.t('pytsite.auth@enter_admin_email') + ': ')
        v = validation.Validator()
        v\
            .add_rule('email', validation.rule.NotEmpty())\
            .add_rule('email', validation.rule.Email()).set_value('email', email)
        if not v.validate():
            raise Exception(v.messages)
        admin_user = _manager.create_user(email)
        admin_user.f_set('full_name', lang.t('pytsite.auth@administrator'))
        admin_user.f_add('roles', _manager.get_role('admin'))
        admin_user.save()
        console.print_success(lang.t('pytsite.auth@user_has_been_created', {'login': admin_user.f_get('login')}))
    except Exception as e:
        raise console.error.ConsoleRuntimeError(e)
