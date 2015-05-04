from pytsite.core.application import wsgi
from pytsite.core import application
import pytsite.auth.plugin as auth

import pytsite.content


def abc():
    user = auth.create_user('a@shepetko.com')
    return user.f_get('login')


application.add_route('/', 'func', abc)

