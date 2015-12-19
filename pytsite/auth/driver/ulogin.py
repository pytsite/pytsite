"""uLogin Auth Driver.
"""
import json as _json
from time import strptime as _strptime
from datetime import datetime as _datetime
from urllib.parse import urlencode as _urlencode
from urllib.request import urlopen as _urlopen
from pytsite import tpl as _tpl, form as _form, reg as _reg, lang as _lang, widget as _widget, http as _http, \
    logger as _logger, router as _router, util as _util, html as _html
from .. import _api, _error
from .abstract import AbstractDriver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _LoginWidget(_widget.Base):
    """ULogin Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._redirect_url = kwargs.get('redirect_url', '')

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        return _html.TagLessElement(_tpl.render('pytsite.auth@drivers/ulogin/widget', {'widget': self}))


class _LoginForm(_form.Form):
    """ULogin Login Form.
    """
    def _setup(self):
        """_setup() hook.
        """
        for k, v in _router.request.inp.items():
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-' + k, name=k, value=v, form_area='hidden'))

        if not self.has_widget(self.uid + '-token'):
            self.add_widget(_widget.input.Hidden(uid=self.uid + '-token', name='token', form_area='hidden'))

        self.add_widget(_LoginWidget(self.uid + '-widget-ulogin'))


class Driver(AbstractDriver):
    """ULogin Driver.
    """
    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'ulogin'

    def get_login_form(self, uid: str, css: str, title: str) -> _form.Form:
        """Get the login form.
        """
        return _LoginForm(uid=uid, css=css, title=title)

    def post_login_form(self, inp: dict) -> _http.response.Redirect:
        """Process submit of the login form.
        """
        # Reading response from uLogin
        response = _urlopen('http://ulogin.ru/token.php?{}'.format(_urlencode(inp)))
        if response.status != 200:
            raise _error.LoginError("Bad response status code from uLogin: {}.".format(response.status))
        ulogin_data = _json.loads(response.read().decode('utf-8'))
        if 'error' in ulogin_data:
            raise _error.LoginError("Bad response from uLogin: '{}'.".format(ulogin_data['error']))
        if 'email' not in ulogin_data or ulogin_data['verified_email'] != '1':
            raise _error.LoginError("Email '{}' is not verified by uLogin.".format(ulogin_data['email']))

        email = ulogin_data['email']
        user = _api.get_user(email)

        try:
            # User is not exists and its creation is not allowed
            if not user and not _reg.get('auth.signup.enabled'):
                raise _error.LoginError(_lang.t('pytsite.auth@signup_is_disabled'))

            # Create new user
            if not user:
                user = _api.create_user(email)

            # Picture
            if not user.f_get('picture'):
                picture_url = ulogin_data['photo_big'] if 'photo_big' in ulogin_data else None
                if not picture_url:
                    picture_url = ulogin_data['photo'] if 'photo' in ulogin_data else None
                if picture_url:
                    from pytsite import image
                    user.f_set('picture', image.create(picture_url))

            # Name
            if not user.first_name and 'first_name' in ulogin_data:
                user.f_set('first_name', ulogin_data['first_name'])
            if not user.last_name and 'last_name' in ulogin_data:
                user.f_set('last_name', ulogin_data['last_name'])

            # Nickname
            if not user.nickname:
                if 'nickname' in ulogin_data:
                    user.f_set('nickname', _util.transform_str_2(ulogin_data['nickname']))
                elif user.first_name and user.last_name:
                    user.f_set('nickname', _util.transform_str_2(user.first_name + '.' + user.last_name))
                elif user.first_name:
                    user.f_set('nickname', _util.transform_str_2(user.first_name))
                else:
                    user.f_set('nickname', _util.transform_str_2(email))

            # Gender
            if not user.gender and 'sex' in ulogin_data:
                user.f_set('gender', int(ulogin_data['sex']))

            # Birth date
            if 'bdate' in ulogin_data:
                b_date = _strptime(ulogin_data['bdate'], '%d.%m.%Y')
                user.f_set('birth_date', _datetime(*b_date[0:5]))

            # Link to profile
            if 'profile' in ulogin_data and ulogin_data['profile']:
                user.f_add('urls', ulogin_data['profile'])

            # Options
            user.options['ulogin'] = ulogin_data

            # Authorize
            _api.authorize(user.save())

            # Unneeded arguments
            if '__form_location' in inp:
                del inp['__form_location']
            if 'token' in inp:
                del inp['token']

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
            if '__form_redirect' in inp:
                del inp['__form_redirect']
            if '__form_location' in inp:
                del inp['__form_location']
            if 'token' in inp:
                del inp['token']

            inp['driver'] = 'ulogin'

            return _http.response.Redirect(_router.ep_url('pytsite.auth.ep.login', args=inp))
