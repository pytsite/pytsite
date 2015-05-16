"""uLogin Auth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json
from urllib.parse import urlencode
from urllib.request import urlopen
from pytsite.core import widgets, tpl, forms, router, reg, lang
from pytsite.image import manager as image_manager
from .. import manager as auth_manager, errors
from .abstract import AbstractDriver


class LoginWidget(widgets.AbstractWidget):
    """ULogin Widget.
    """

    def __init__(self, uid: str, **kwargs: dict):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._redirect_url = kwargs.get('redirect_url', '')

    def render(self)->str:
        """Render the widget.
        """
        return tpl.render('pytsite.auth@drivers/ulogin/widget', {'widget': self})


class LoginForm(forms.AbstractForm):
    """ULogin Login Form.
    """

    def _setup(self):
        """_setup() hook.
        """

        self._add_widget(widgets.HiddenInput(uid=self.uid + '-token', name='token'))
        for k, v in router.request.values.items():
            self._add_widget(widgets.HiddenInput(uid=self.uid + '-' + k, name=k, value=v))

        self._add_widget(LoginWidget('ulogin-widget'))


class ULoginDriver(AbstractDriver):
    """ULogin Driver.
    """

    def get_login_form(self, uid: str) -> forms.AbstractForm:
        """Get the login form.
        """

        return LoginForm(uid=uid)

    def post_login_form(self, args: dict, inp: dict)->router.RedirectResponse:
        """Process submit of the login form.
        """

        # Reading response from uLogin
        response = urlopen('http://ulogin.ru/token.php?{0}'.format(urlencode(inp)))
        if response.status != 200:
            raise Exception("Bad response status code from uLogin: {0}.".format(response.status))
        ulogin_data = json.loads(response.read().decode('utf-8'))
        if 'error' in ulogin_data:
            raise Exception("Bad response from uLogin: '{0}'.".format(ulogin_data['error']))
        if 'email' not in ulogin_data or ulogin_data['verified_email'] != '1':
            raise Exception("Email '{0}' is not verified by uLogin.".format(ulogin_data['email']))

        email = ulogin_data['email']
        user = auth_manager.get_user(email)

        try:
            # User is not exists and its creation is not allowed
            if not user and not reg.get_val('auth.auto_signup'):
                raise errors.LoginIncorrect()

            # Create new user
            if not user:
                user = auth_manager.create_user(login=email, email=email)

                # Picture
                picture_url = ulogin_data['photo_big'] if 'photo_big' in ulogin_data else None
                if not picture_url:
                    picture_url = ulogin_data['photo'] if 'photo' in ulogin_data else None
                if picture_url:
                    user.f_set('picture', image_manager.create(picture_url))

                # Full name
                full_name = ''
                if 'first_name' in ulogin_data:
                    full_name += ulogin_data['first_name']
                if 'last_name' in ulogin_data:
                    full_name += ' ' + ulogin_data['last_name']
                user.f_set('fullName', full_name)

                # Gender
                if 'sex' in ulogin_data:
                    user.f_set('gender', ulogin_data['sex'])

                # Options
                user.f_set('options', {'ulogin': ulogin_data})

                user.save()

            # Unneeded uLogin token
            if 'token' in inp:
                del inp['token']

            # Authorize
            auth_manager.authorize(user)

            # Redirect to the final destination
            if 'redirect' in inp:
                redirect = inp['redirect']
                del inp['redirect']
                return router.RedirectResponse(router.url(redirect, query=inp))

        except errors.LoginIncorrect:
            router.session.add_error(lang.t('pytsite.auth@authorization_error'))
            return router.RedirectResponse(router.endpoint_url('pytsite.auth.endpoints.get_login', args=inp))
