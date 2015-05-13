"""uLogin Auth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json
from urllib.parse import urlencode
from urllib.request import urlopen
from pytsite.core import widget, tpl, forms, router
from pytsite.image import manager as image_manager
from .. import manager as auth_manager
from .. import errors
from .abstract import AbstractDriver


class LoginWidget(widget.AbstractWidget):
    """ULogin login widget.
    """
    def render(self)->str:
        """Render the widget.
        """
        return tpl.render('pytsite.auth@drivers/ulogin/widget')


class LoginForm(forms.AbstractForm):
    """ULogin login form.
    """
    def _setup(self):
        self._add_widget(LoginWidget('ulogin-widget'))


class ULoginDriver(AbstractDriver):
    """ULogin driver.
    """
    def get_login_form(self)->forms.AbstractForm:
        """Get the login form.
        """
        return LoginForm(uid='ulogin-form')

    def post_login_form(self, args: dict, inp: dict)->router.RedirectResponse:
        """Post the login form.
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
        if not user:
            user = auth_manager.create_user(login=email, email=email)

            picture_url = ulogin_data['photo_big'] if 'photo_big' in ulogin_data else None
            if not picture_url:
                picture_url = ulogin_data['photo'] if 'photo' in ulogin_data else None

            if picture_url:
                user.f_set('picture', image_manager.create(picture_url))

            full_name = ''
            if 'first_name' in ulogin_data:
                full_name += ulogin_data['first_name']
            if 'last_name' in ulogin_data:
                full_name += ' ' + ulogin_data['last_name']
            user.f_set('fullName', full_name)

            if 'sex' in ulogin_data:
                user.f_set('gender', ulogin_data['sex'])

            user.f_set('options', {'ulogin': ulogin_data})

            user.save()

        auth_manager.authorize(user)