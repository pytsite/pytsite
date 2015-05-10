from ..core import odm
from .models import User


def create_user(login: str)->User:
    user = odm.dispense('user')
    user.f_set('login', login)
    return user