"""Event Handlers.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang as _lang, console as _console, validation as _validation
from . import _functions


def app_setup():
    """'app.setup' Event Handler.
    """
    # Creating roles
    admin_role = ('admin', 'pytsite.auth@admin_role_description')
    user_role = ('user', 'pytsite.auth@user_role_description')
    for role in admin_role, user_role:
        if not _functions.get_role(name=role[0]):
            role_entity = _functions.create_role(role[0], role[1])
            if role_entity.f_get('name') == 'admin':
                role_entity.f_add('permissions', 'admin')
            role_entity.save()
            _console.print_success(_lang.t('auth@role_has_been_created',
                                                     {'name': role_entity.f_get('name')}))

    # Creating administrator
    try:
        email = input(_lang.t('auth@enter_admin_email') + ': ')
        v = _validation.Validator()
        v\
            .add_rule('email', _validation.rule.NotEmpty())\
            .add_rule('email', _validation.rule.Email()).set_value('email', email)
        if not v.validate():
            raise Exception(v.messages)
        admin_user = _functions.create_user(email)
        admin_user.f_set('full_name', _lang.t('auth@administrator'))
        admin_user.f_add('roles', _functions.get_role('admin'))
        admin_user.save()
        _console.print_success(_lang.t('auth@user_has_been_created',
                                                 {'login': admin_user.f_get('login')}))
    except Exception as e:
        raise _console.error.ConsoleRuntimeError(e)
