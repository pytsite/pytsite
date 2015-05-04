from ..core import odm
from . import models

odm.register_model('user', models.User)


def create_user(login: str):
    user = odm.dispense('user')
    user.f_set('login', login)
    return user