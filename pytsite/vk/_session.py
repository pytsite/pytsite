"""VK Session.
"""
import requests as _requests
from os import path as _path
from pytsite import reg as _reg, image as _image
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Session:
    _method_base_url = 'https://api.vk.com/method/'

    def __init__(self, access_token: str, app_id: str=None, app_secret: str=None):
        """Init.
        """
        self._access_token = access_token
        self._app_id = app_id or _reg.get('vk.app_id')
        self._app_secret = app_secret or _reg.get('vk.app_secret')

    def request(self, method: str, **kwargs):
        """Perform a request to the VK API.
        """
        kwargs['access_token'] = self._access_token
        r = _requests.get(self._method_base_url + method, kwargs)

        if r.status_code != 200:
            raise _error.RequestError(r.content)

        r = r.json()
        if 'error' in r:
            raise _error.MethodError(str(r['error']))

        return r['response']

    def get_users_info(self, users_ids: tuple, fields: tuple=None) -> list:
        """Get info anout multiple users.
        """
        return self.request('users.get', users_ids=users_ids, fields=fields)

    def get_user_info(self, user_id: int, fields: tuple=None):
        """Get info about user.
        """
        return self.get_users_info((user_id,), fields)[0]

    def get_screen_name(self, user_id: int) -> str:
        """Get screen name of the user.
        """
        return self.get_user_info(user_id, fields=('screen_name',))['screen_name']

    def photos_get_wall_upload_server(self, group_id: int=None) -> str:
        """Get URL of the server to upload walls' photo.
        """
        return self.request('photos.getWallUploadServer', group_id=group_id)['upload_url']

    def wall_upload_photo(self, photo, user_id: int=None, group_id: int=0, name: str=None) -> dict:
        """Upload a photo to the user's or community's wall wall.

        :type photo: image.model.Image | str
        """
        if isinstance(photo, _image.model.Image):
            file = open(photo.abs_path, 'rb')
            if not name:
                name = _path.basename(photo.abs_path)
        elif isinstance(photo, str):
            file = open(photo, 'rb')
            if not name:
                name = _path.basename(photo)
        else:
            raise TypeError('pytsite.image.model.Image or str expected.')

        group_id = abs(group_id)
        r = _requests.post(self.photos_get_wall_upload_server(group_id), files={'photo': (name, file)}).json()

        if file:
            file.close()

        return self.request('photos.saveWallPhoto', user_id=user_id, group_id=group_id, server=r['server'],
                            hash=r['hash'], photo=r['photo'])[0]

    def wall_post(self, owner_id: int, message: str=None, photo=None, photo_link: str=None) -> int:
        """Post message to the user's or community's wall.

        :type photo: _image.model.Image | str
        """
        args = {
            'owner_id': owner_id,
            'message': message,
        }

        if owner_id < 0:
            args['from_group'] = 1

        if photo:
            if owner_id > 0:
                attach = self.wall_upload_photo(photo, user_id=owner_id)['id']
            else:
                attach = self.wall_upload_photo(photo, group_id=owner_id)['id']

            if photo_link:
                attach += ',' + photo_link

            args['attachments'] = attach

        return self.request('wall.post', **args)['post_id']
