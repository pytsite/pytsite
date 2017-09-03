"""PytSite Auth Event Handlers
"""
from pytsite import lang as _lang, console as _console, validation as _validation, util as _util
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def setup():
    """'pytsite.setup' Event Handler
    """
    # Search for an administrator
    if _api.count_users({'roles': [_api.get_role('admin')]}):
        return

    # Create administrator
    email = input(_lang.t('pytsite.auth@enter_admin_email') + ': ')
    try:
        _validation.rule.NonEmpty(email, 'pytsite.auth@email_cannot_be_empty').validate()
        _validation.rule.Email(email).validate()
    except _validation.error.RuleError as e:
        raise _console.error.Error(e)

    _api.switch_user_to_system()
    admin_user = _api.create_user(email)
    admin_user.first_name = _lang.t('pytsite.auth@administrator')
    admin_user.nickname = _util.transform_str_2(admin_user.full_name)
    admin_user.roles = [_api.get_role('admin')]
    admin_user.save()
    _api.restore_user()
    _console.print_success(_lang.t('pytsite.auth@user_has_been_created', {'login': admin_user.login}))

    # Set password for created admin
    _console.run_command('auth:passwd', arguments=[admin_user.login])
