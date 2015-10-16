"""VK Session.
"""
import requests
from pytsite import reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Session():
    _method_url = 'https://api.vk.com/method/'

    def __init__(self, access_token: str=None, app_id: str=None, app_secret: str=None):
        self._access_token = access_token
        self._app_id = app_id or _reg.get('vk.app_id')
        self._app_secret = app_id or _reg.get('vk.app_secret')

    def get_user_info(self, user_id: int, fields: tuple=None):
        r = requests.get(self._method_url + 'users.get', {
            'access_token': self._access_token,
            'users_ids': user_id,
            'fields': fields,
        }).json()

        if 'error' in r:
            raise Exception(str(r['error']))

        return r['response'][0]

    def get_screen_name(self, user_id: int) -> str:
        return self.get_user_info(user_id, fields=('screen_name',))['screen_name']

    def wall_post(self, owner_id: int=None, message: str=None, attachments: list=None):
        r = requests.get(self._method_url + 'wall.post', {
            'owner_id': owner_id,
            'access_token': self._access_token,
            'message': message,
        })

        print(r.status_code)
        print(r.content)
