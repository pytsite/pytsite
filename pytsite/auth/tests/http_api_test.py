"""
"""
from pytsite import unittest, http_api, auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class HttpApiTest(unittest.TestCase):
    def test_get_access_token(self):
        token = auth.generate_access_token(auth.get_user('user1@test.com'))

        url = http_api.url('pytsite.auth@get_access_token', {'token': token})
        resp = self.send_http_request(self.prepare_http_request('GET', url))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'expires')
        self.assertHttpRespJsonFieldNotEmpty(resp, 'user_uid')
        self.assertHttpRespJsonFieldIsInt(resp, 'ttl')
        self.assertHttpRespJsonFieldEquals(resp, 'token', token)

    def test_delete_access_token(self):
        token = auth.generate_access_token(auth.get_user('user1@test.com'))
        url = http_api.url('pytsite.auth@delete_access_token', {'token': token})
        resp = self.send_http_request(self.prepare_http_request('DELETE', url))
        self.assertHttpRespJsonFieldIsTrue(resp, 'status')

        with self.assertRaises(auth.error.InvalidAccessToken):
            auth.get_access_token_info(token)

    def test_get_user(self):
        user = auth.get_user('user1@test.com')
        token = auth.generate_access_token(auth.get_user('user1@test.com'))
        url = http_api.url('pytsite.auth@get_user', {'uid': user.uid})
        resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': token}))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldNotEmpty(resp, 'uid')

        self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
        self.assertHttpRespJsonFieldIsEmail(resp, 'login')
        self.assertHttpRespJsonFieldIsEmail(resp, 'email')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'last_sign_in')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'last_activity')
        self.assertHttpRespJsonFieldIsInt(resp, 'sign_in_count')
        self.assertHttpRespJsonFieldEquals(resp, 'status', 'active')
        self.assertHttpRespJsonFieldIsBool(resp, 'profile_is_public')
        self.assertHttpRespJsonFieldIsList(resp, 'roles')

        self.assertHttpRespJsonFieldIsStr(resp, 'profile_url')
        self.assertHttpRespJsonFieldIsStr(resp, 'nickname')
        self.assertHttpRespJsonFieldIsStr(resp, 'first_name')
        self.assertHttpRespJsonFieldIsStr(resp, 'last_name')
        self.assertHttpRespJsonFieldIsStr(resp, 'full_name')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'birth_date')
        self.assertHttpRespJsonFieldIsStr(resp, 'gender')
        self.assertHttpRespJsonFieldIsStr(resp, 'phone')
        self.assertHttpRespJsonFieldIsList(resp, 'follows')
        self.assertHttpRespJsonFieldIsList(resp, 'followers')
        self.assertHttpRespJsonFieldIsDict(resp, 'picture')
        self.assertHttpRespJsonFieldIsList(resp, 'urls')

    def test_post_follow(self):
        user1 = auth.get_user('user1@test.com')
        user2 = auth.get_user('user2@test.com')
        user1_token = auth.generate_access_token(user1)

        url = http_api.url('pytsite.auth@post_follow', {'uid': user2.uid})
        resp = self.send_http_request(self.prepare_http_request('POST', url, {'PytSite-Auth': user1_token}))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsList(resp, 'follows')
        self.assertHttpRespJsonFieldNotEmpty(resp, 'follows')

    def test_delete_follow(self):
        user1 = auth.get_user('user1@test.com')
        user2 = auth.get_user('user2@test.com')
        user1_token = auth.generate_access_token(user1)

        user1.add_follows(user2)

        url = http_api.url('pytsite.auth@delete_follow', {'uid': user2.uid})
        resp = self.send_http_request(self.prepare_http_request('DELETE', url, {'PytSite-Auth': user1_token}))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsList(resp, 'follows')
        self.assertHttpRespJsonFieldIsEmpty(resp, 'follows')
