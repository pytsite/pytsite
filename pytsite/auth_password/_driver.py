"""PytSite Auth Password Driver.
"""
from pytsite import auth as _auth, form as _form, router as _router, widget as _widget, lang as _lang, \
    logger as _logger, assetman as _assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _SignInForm(_form.Form):
    """Password Login Form.
    """

    def _on_setup_form(self, **kwargs):
        self.area_footer_css = 'text-center'

    def _on_setup_widgets(self):
        """Hook.
        """
        for k, v in _router.request().inp.items():
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-' + k, name=k, value=v, form_area='hidden'))

        self.add_widget(_widget.input.Email(
            uid='login',
            weight=10,
            label=_lang.t('pytsite.auth_password@login'),
            prepend='<i class="fa fa-user"></i>',
            h_size='col-xs-12 col-sm-6 col-sm-offset-3',
            h_size_label=True,
            required=True,
            value=_router.request().inp.get('login', ''),
        ))

        self.add_widget(_widget.input.Password(
            uid='password',
            weight=20,
            label=_lang.t('pytsite.auth_password@password'),
            prepend='<i class="fa fa-lock"></i>',
            h_size='col-xs-12 col-sm-6 col-sm-offset-3',
            h_size_label=True,
            required=True,
        ))

        submit_btn = self.get_widget('action-submit')
        submit_btn.value = _lang.t('pytsite.auth_password@sign_in')
        submit_btn.icon = 'fa fa-sign-in'


class Password(_auth.driver.Authentication):
    """ULogin Driver.
    """

    def get_name(self) -> str:
        """Get name of the driver
        """
        return 'password'

    def get_description(self) -> str:
        """Get name of the driver
        """
        return 'Password'

    def get_sign_up_form(self, **kwargs) -> _form.Form:
        # TODO
        pass

    def get_sign_in_form(self, **kwargs) -> _form.Form:
        """Get the login form.
        """
        _assetman.preload('font-awesome')

        return _SignInForm(**kwargs)

    def sign_up(self, data: dict):
        # TODO
        pass

    def sign_in(self, data: dict) -> _auth.model.AbstractUser:
        """Authenticate user.
        """
        login = data.get('login')
        password = data.get('password')

        if not (login and password):
            raise _auth.error.AuthenticationError('Login or password is not specified')

        # Check if the user exists
        user = _auth.get_user(login)
        if not user:
            _logger.warn("User with login '{}' is not found".format(login))
            raise _auth.error.AuthenticationError(_lang.t('pytsite.auth@authentication_error'))

        # Check password
        if not _auth.verify_password(password, user.password):
            _logger.warn("Incorrect password provided for user with login '{}'".format(login))
            raise _auth.error.AuthenticationError(_lang.t('pytsite.auth@authentication_error'))

        return user
