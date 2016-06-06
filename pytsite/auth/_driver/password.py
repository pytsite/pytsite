"""Password Auth Driver.
"""
from pytsite import form as _form, lang as _lang, widget as _widget, router as _router
from .. import _api, _error, _model
from .abstract import Abstract

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _SignInForm(_form.Form):
    """Password Login Form.
    """
    def _setup_widgets(self):
        """Hook.
        """
        for k, v in _router.request().inp.items():
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-' + k, name=k, value=v, form_area='hidden'))

        self.add_widget(_widget.input.Email(
            uid='login',
            label=_lang.t('pytsite.auth@email'),
            weight=10,
            required=True,
            value=_router.request().inp.get('login', ''),
        ))

        self.add_widget(_widget.input.Password(
            uid='password',
            label=_lang.t('pytsite.auth@password'),
            weight=20,
            required=True,
        ))

        self.get_widget('action-submit').value = _lang.t('pytsite.auth@login')


class Password(Abstract):
    """ULogin Driver.
    """
    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'password'

    def get_sign_up_form(self, form_uid: str, **kwargs) -> _form.Form:
        # TODO
        pass

    def get_sign_in_form(self, form_uid: str, **kwargs) -> _form.Form:
        """Get the login form.
        """
        return _SignInForm(uid=form_uid, **kwargs)

    def sign_up(self, data: dict):
        # TODO
        pass

    def sign_in(self, data: dict) -> _model.User:
        """Authenticate user.
        """
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            raise _error.AuthenticationError('Login or password is not specified.')

        # Check if the user exists
        user = _api.get_user(login)
        if not user:
            raise _error.AuthenticationError(_lang.t('pytsite.auth@authentication_error'))

        # Check password
        if not _api.verify_password(password, user.password):
            raise _error.AuthenticationError(_lang.t('pytsite.auth@authentication_error'))

        return user

    def sign_out(self, user: _model.User):
        """End user's session.
        """
        pass
