"""Password Auth Driver.
"""
from pytsite import form as _form, lang as _lang, widget as _widget, http as _http, logger as _logger, router as _router
from .. import _api, _error
from .abstract import AbstractDriver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _LoginForm(_form.Base):
    """Password Login Form.
    """
    def _setup(self):
        """_setup() hook.
        """
        for k, v in _router.request.inp.items():
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-' + k, name=k, value=v, form_area='hidden'))

        self.add_widget(_widget.input.Email(
            uid='email',
            label=_lang.t('pytsite.auth@email'),
            weight=10,
            required=True,
            value=_router.request.inp.get('email', ''),
        ))

        self.add_widget(_widget.input.Password(
            uid='password',
            label=_lang.t('pytsite.auth@password'),
            weight=20,
            required=True,
        ))

        self.add_widget(_widget.button.Submit(
            value=_lang.t('pytsite.auth@login'),
            form_area='footer',
        ))


class Driver(AbstractDriver):
    """ULogin Driver.
    """
    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'password'

    def get_login_form(self, uid, css, title) -> _form.Base:
        """Get the login form.
        """
        return _LoginForm(uid=uid, css=css, title=title)

    def post_login_form(self, inp: dict) -> _http.response.Redirect:
        """Process submit of the login form.
        """
        try:
            email = inp.get('email')
            password = inp.get('password')
            user = _api.get_user(email)

            # Unneeded arguments
            for i in ('__form_location', 'email', 'password'):
                if i in inp:
                    del inp[i]

            # User is not exists
            if not user:
                raise _error.LoginError(_lang.t('pytsite.auth@authorization_error'))

            # Bad password
            if not _api.password_verify(password, user.password):
                raise _error.LoginError(_lang.t('pytsite.auth@authorization_error'))

            _api.authorize(user)

            # Redirect to the final destination
            if 'redirect' in inp:
                redirect = inp['redirect']
                del inp['redirect']
                if '__form_redirect' in inp:
                    del inp['__form_redirect']
                return _http.response.Redirect(_router.url(redirect, query=inp))
            elif '__form_redirect' in inp:
                redirect = inp['__form_redirect']
                del inp['__form_redirect']
                return _http.response.Redirect(_router.url(redirect, query=inp))
            else:
                return _http.response.Redirect(_router.base_url(query=inp))

        except _error.LoginError as e:
            _logger.warn('Login incorrect. {}'.format(e), __name__)
            _router.session.add_error(_lang.t('pytsite.auth@authorization_error'))

            # Unneeded arguments
            for i in ('__form_redirect',):
                if i in inp:
                    del inp[i]

            inp['driver'] = self.name
            return _http.response.Redirect(_router.ep_url('pytsite.auth.ep.login', args=inp))