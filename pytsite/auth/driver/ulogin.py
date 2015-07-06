"""uLogin Auth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json as _json
from time import strptime as _strptime
from datetime import datetime as _datetime
from urllib.parse import urlencode as _urlencode
from urllib.request import urlopen as _urlopen
from pytsite.core import tpl as _tpl, form as _form, router as _router, reg as _reg, lang as _lang, \
    widget as _widget, http as _http, client as _client
from pytsite import image as _image
from .. import _functions, _error
from .abstract import AbstractDriver


class Login(_widget.Base):
    """ULogin Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__()
        self._redirect_url = kwargs.get('redirect_url', '')

    def render(self) -> str:
        """Render the widget.
        """
        return _tpl.render('pytsite.auth@drivers/ulogin/widget', {'widget': self})


class LoginForm(_form.Base):
    """ULogin Login Form.
    """
    def _setup(self):
        """_setup() hook.
        """
        for k, v in _router.request.values.items():
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-' + k, name=k, value=v))

        if not self.has_widget(self.uid + '-token'):
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-token', name='token'))

        self.add_widget(Login())


class ULoginDriver(AbstractDriver):
    """ULogin Driver.
    """
    def get_login_form(self, uid: str='pytsite-auth-login', cls: str=None) -> _form.Base:
        """Get the login form.
        """
        return LoginForm(uid=uid, cls=cls)

    def post_login_form(self, args: dict, inp: dict) -> _http.response.RedirectResponse:
        """Process submit of the login form.
        """

        # Reading response from uLogin
        response = _urlopen('http://ulogin.ru/token.php?{0}'.format(_urlencode(inp)))
        if response.status != 200:
            raise Exception("Bad response status code from uLogin: {0}.".format(response.status))
        ulogin_data = _json.loads(response.read().decode('utf-8'))
        if 'error' in ulogin_data:
            raise Exception("Bad response from uLogin: '{0}'.".format(ulogin_data['error']))
        if 'email' not in ulogin_data or ulogin_data['verified_email'] != '1':
            raise Exception("Email '{0}' is not verified by uLogin.".format(ulogin_data['email']))

        email = ulogin_data['email']
        user = _functions.get_user(email)

        try:
            # User is not exists and its creation is not allowed
            if not user and not _reg.get('auth.allow_signup'):
                raise _error.LoginIncorrect()

            # Create new user
            if not user:
                user = _functions.create_user(login=email, email=email)

            # Picture
            if not user.f_get('picture'):
                picture_url = ulogin_data['photo_big'] if 'photo_big' in ulogin_data else None
                if not picture_url:
                    picture_url = ulogin_data['photo'] if 'photo' in ulogin_data else None
                if picture_url:
                    user.f_set('picture', _image.manager.create(picture_url))

            # Name
            full_name = ''
            if 'first_name' in ulogin_data:
                user.f_set('first_name', ulogin_data['first_name'])
                full_name += ulogin_data['first_name']
            if 'last_name' in ulogin_data:
                user.f_set('last_name', ulogin_data['last_name'])
                full_name += ' ' + ulogin_data['last_name']
            user.f_set('full_name', full_name)

            # Gender
            if 'sex' in ulogin_data:
                user.f_set('gender', int(ulogin_data['sex']))

            # Birth date
            if 'bdate' in ulogin_data:
                b_date = _strptime(ulogin_data['bdate'], '%d.%m.%Y')
                user.f_set('birth_date', _datetime(*b_date[0:5]))

            # Options
            user.f_set('options', {'ulogin': ulogin_data})

            # Unneeded uLogin token
            if 'token' in inp:
                del inp['token']

            # Authorize
            user.save()
            _functions.authorize(user)

            # Saving statistical information
            user.f_add('login_count', 1).f_set('last_login', _datetime.now()).save()

            if '__form_redirect' in inp:
                del inp['__form_redirect']

            # Redirect to the final destination
            if 'redirect' in inp:
                redirect = inp['redirect']
                del inp['redirect']
                del inp['__form_location']
                return _http.response.RedirectResponse(_router.url(redirect, query=inp))
            elif '__form_location' in inp:
                redirect = inp['__form_location']
                del inp['__form_location']
                return _http.response.RedirectResponse(_router.url(redirect, query=inp))
            else:
                return _http.response.RedirectResponse(_router.base_url(query=inp))

        except _error.LoginIncorrect:
            _router.session.add_error(_lang.t('pytsite.auth@authorization_error'))
            return _http.response.RedirectResponse(_router.endpoint_url('pytsite.auth.eps.get_login', args=inp))
