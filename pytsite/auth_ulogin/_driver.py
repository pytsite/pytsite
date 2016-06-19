"""uLogin Auth Driver.
"""
import json as _json
from time import strptime as _strptime
from datetime import datetime as _datetime
from urllib.request import urlopen as _urlopen
from pytsite import tpl as _tpl, form as _form, reg as _reg, lang as _lang, widget as _widget, router as _router, \
    html as _html, auth as _auth

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

        self._assets.append('pytsite.auth_ulogin@css/widget.css')
        self._css += 'widget-ulogin'

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return _html.TagLessElement(_tpl.render('pytsite.auth_ulogin@widget', {'widget': self}))


class _LoginForm(_form.Form):
    """ULogin Login Form.
    """
    def _setup_widgets(self):
        """_setup() hook.
        """
        self.add_widget(_widget.input.Hidden(
            uid=self.uid + '-widget-ulogin-token',  # It is important ID format fo JS code. Don't change!
            form_area='hidden',
            required=True,
        ))

        # uLogin widget
        self.add_widget(_LoginWidget(
            uid=self.uid + '-widget-ulogin'  # It is important ID format fo JS code. Don't change!
        ))

        # Submit button is not necessary, form submit performs by JS code
        self.remove_widget('action-submit')


class ULogin(_auth.driver.Authentication):
    """ULogin Driver.
    """
    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'ulogin'

    def get_sign_up_form(self, form_uid: str, **kwargs) -> _form.Form:
        """Get the sign up form form.
        """
        return _LoginForm(uid=form_uid, **kwargs)

    def get_sign_in_form(self, form_uid: str, **kwargs) -> _form.Form:
        """Get the sign in form form.
        """
        return self.get_sign_up_form(form_uid, **kwargs)

    def sign_up(self, data: dict) -> _auth.model.UserInterface:
        # Searching for token in input data
        token = data.get('token')
        if not token:
            for k, v in data.items():
                if k.endswith('token'):
                    token = v
                    break

        if not token:
            raise ValueError('No uLogin token.')

        # Getting user's data from uLogin
        response = _urlopen('http://ulogin.ru/token.php?token={}&host={}'.format(token, _router.request().host))
        if response.status != 200:
            raise _auth.error.AuthenticationError("Bad response status code from uLogin: {}.".format(response.status))
        ulogin_data = _json.loads(response.read().decode('utf-8'))
        if 'error' in ulogin_data:
            raise _auth.error.AuthenticationError("Bad response from uLogin: '{}'.".format(ulogin_data['error']))
        if 'email' not in ulogin_data or ulogin_data['verified_email'] != '1':
            raise _auth.error.AuthenticationError("Email '{}' is not verified by uLogin.".format(ulogin_data['email']))

        email = ulogin_data['email']

        try:
            user = _auth.get_user(email)

        except _auth.error.UserNotExist:
            # User is not exists and its creation is not allowed
            if not _reg.get('auth.signup.enabled'):
                raise _auth.error.AuthenticationError(_lang.t('pytsite.auth_ulogin@signup_is_disabled'))
            else:
                # New users can be created only by system user
                _auth.switch_user(_auth.get_system_user())

                # Create new user
                user = _auth.create_user(email)

        # As soon as user created or loaded, set it as current
        _auth.switch_user(user)

        # Picture
        if not user.picture:
            picture_url = ulogin_data.get('photo_big')
            if not picture_url:
                picture_url = ulogin_data.get('photo')
            if picture_url:
                from pytsite import image
                user.picture = image.create(picture_url)

        # Name
        if not user.first_name and 'first_name' in ulogin_data:
            user.first_name = ulogin_data['first_name']
        if not user.last_name and 'last_name' in ulogin_data:
            user.last_name = ulogin_data['last_name']

        # Alter nickname
        if user.is_new:
            user.nickname = user.full_name

        # Gender
        if user.gender not in ('m', 'f') and 'sex' in ulogin_data:
            user.gender = 'f' if int(ulogin_data['sex']) == 1 else 'm'

        # Birth date
        if 'bdate' in ulogin_data:
            b_date = _strptime(ulogin_data['bdate'], '%d.%m.%Y')
            user.birth_date = _datetime(*b_date[0:5])

        # Link to profile
        if 'profile' in ulogin_data and ulogin_data['profile']:
            user.urls = (ulogin_data['profile'],)

        # Options
        options = dict(user.options)
        options['ulogin'] = ulogin_data
        user.options = options

        return user

    def sign_in(self, data: dict) -> _auth.model.UserInterface:
        """Authenticate user.
        """
        return self.sign_up(data)
