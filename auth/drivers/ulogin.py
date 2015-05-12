"""uLogin Auth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from urllib.parse import urlencode
from .abstract import AbstractDriver
from ...core import tpl
from ...core.router import Request, RedirectResponse
from ...core.widget import AbstractWidget
from ...core.form import AbstractForm


class LoginWidget(AbstractWidget):
    """ULogin login widget.
    """
    def render(self)->str:
        """Render the widget.
        """
        return tpl.render('pytsite.auth@drivers/ulogin/widget')


class LoginForm(AbstractForm):
    """ULogin login form.
    """
    def _setup(self):
        self._add_widget(LoginWidget('ulogin-widget'))


class ULoginDriver(AbstractDriver):
    """ULogin driver.
    """
    def get_login_form(self)->AbstractForm:
        """Get the login form.
        """
        return LoginForm(uid='ulogin-form')

    def post_login_form(self, args: dict, inp: dict)->RedirectResponse:
        """Post the login form.
        """
        from urllib.request import urlopen

        response = urlopen('http://ulogin.ru/token.php?{0}'.format(urlencode(inp)))
        if response.status != 200:
            raise Exception("Bad response status code from uLogin: {0}.".format(response.status))

        from json import loads
        data = loads(response.read().decode('utf-8'))
        if 'error' in data:
            raise Exception("Bad response from uLogin: '{0}'.".format(data['error']))

        if 'email' not in data or data['verified_email'] != '1':
            raise Exception("Email '{0}' is not verified by uLogin.".format(data['email']))

        from .. import manager as user_manager
        login = data['email']
        user = user_manager.get_user_by_login(login)
        if not user:
            user = user_manager.create_user(login, login)
            picture_url = data['photo_big'] if 'photo_big' in data else None
            if not picture_url:
                picture_url = data['photo'] if 'photo' in data else None

            if picture_url:
                from ...image import manager as img_manager
                user.f_set('picture', img_manager.create(picture_url))

            user.save()