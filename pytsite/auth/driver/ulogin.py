"""uLogin Auth Driver.
"""
import json as _json
from time import strptime as _strptime
from datetime import datetime as _datetime
from urllib.request import urlopen as _urlopen
from pytsite import tpl as _tpl, form as _form, reg as _reg, lang as _lang, widget as _widget, http as _http, \
    logger as _logger, router as _router, html as _html
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

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return _html.TagLessElement(_tpl.render('pytsite.auth@drivers/ulogin/widget', {'widget': self}))


class _LoginForm(_form.Form):
    """ULogin Login Form.
    """
    def _setup_widgets(self):
        """_setup() hook.
        """
        self.add_widget(_widget.input.Hidden(
            uid=self.uid + '-widget-ulogin-token',
            form_area='hidden',
            required=True,
        ))

        # uLogin widget
        self.add_widget(_LoginWidget(
            uid=self.uid + '-widget-ulogin'
        ))

        # Action buttons is not necessary, form submitting initiates via JS code
        self.remove_widget('action-submit')


class Driver(AbstractDriver):
    """ULogin Driver.
    """
    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'ulogin'

    def get_login_form(self, uid: str, **kwargs) -> _form.Form:
        """Get the login form.
        """
        return _LoginForm(uid=uid, **kwargs)

    def post_login_form(self, inp: dict) -> _http.response.Redirect:
        """Process submit of the login form.
        """
        token = ''
        for k, v in inp.items():
            if k.endswith('-widget-ulogin-token'):
                token = v
                del inp[k]
                break

        if not token:
            raise ValueError('No token received.')

        # Reading response from uLogin
        response = _urlopen('http://ulogin.ru/token.php?token={}&host={}'.format(token, _router.request().host))
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
            options = dict(user.options)
            options['ulogin'] = ulogin_data
            user.f_set('options', options)

            # Authorize
            _api.authorize(user.save())

            # Unneeded arguments
            if 'token' in inp:
                del inp['token']

            # Redirect to the final destination
            if '__redirect' in inp:
                redirect = inp['__redirect']
                del inp['__redirect']
                return _http.response.Redirect(_router.url(redirect, query=inp))
            else:
                return _http.response.Redirect(_router.base_url(query=inp))

        except _error.LoginError as e:
            _logger.warn('Login incorrect. {}'.format(e), __name__)
            _router.session().add_error(_lang.t('pytsite.auth@authorization_error'))
            if '__redirect' in inp:
                del inp['__redirect']
            if 'token' in inp:
                del inp['token']

            inp['driver'] = 'ulogin'

            return _http.response.Redirect(_router.ep_url('pytsite.auth.ep.login', args=inp))
