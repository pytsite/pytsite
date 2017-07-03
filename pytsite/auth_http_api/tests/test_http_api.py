"""PytSite Auth HTTP API Tests
"""
import json
from datetime import datetime
from pytsite import testing, http_api, auth, util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestHttpApi(testing.TestCase):
    """PytSite Auth HTTP API Tests
    """

    def setUp(self):
        """Setup
        """
        auth.switch_user_to_system()

        for i in range(1, 4):
            user = auth.create_user('test_user_{}@test.com'.format(i), 'test_user_{}_password'.format(i))
            user.set_field('nickname', 'nickname-{}'.format(i))
            user.set_field('first_name', 'first_name_{}'.format(i))
            user.set_field('last_name', 'last_name_{}'.format(i))
            user.set_field('description', 'description_{}'.format(i))
            user.set_field('birth_date', datetime(1984, 7, i, i, i, i))
            user.set_field('gender', 'm' if i in (1, 3) else 'f')
            user.set_field('phone', '+3801234567{}'.format(i))
            user.set_field('urls', ['http://test.com/user-{}'.format(i)])
            user.set_field('country', 'Ukraine')
            user.set_field('city', 'Kyiv')
            user.save()

        auth.restore_user()

    def tearDown(self):
        """Tear down
        """
        auth.switch_user_to_system()

        for i in range(1, 4):
            auth.get_user('test_user_{}@test.com'.format(i)).delete()

        auth.restore_user()

    def get_user_via_http(self, login: str):
        user = auth.get_user(login)
        token = auth.generate_access_token(user)
        url = http_api.url('pytsite.auth@get_user', {'uid': user.uid})

        return self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': token}))

    def test_post_access_token(self):
        """POST auth/access-token/<driver>

        There is no code because it should be implemented by authentication drivers
        """
        pass

    def test_get_access_token(self):
        """GET auth/access-token/<token>
        """
        token = auth.generate_access_token(auth.get_user('test_user_1@test.com'))

        url = http_api.url('pytsite.auth@get_access_token', {'token': token})
        resp = self.send_http_request(self.prepare_http_request('GET', url))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'expires')
        self.assertHttpRespJsonFieldNotEmpty(resp, 'user_uid')
        self.assertHttpRespJsonFieldIsInt(resp, 'ttl')
        self.assertHttpRespJsonFieldEquals(resp, 'token', token)

    def test_delete_access_token(self):
        """DELETE auth/access-token/<token>
        """
        token = auth.generate_access_token(auth.get_user('test_user_1@test.com'))
        url = http_api.url('pytsite.auth@delete_access_token', {'token': token})
        resp = self.send_http_request(self.prepare_http_request('DELETE', url))
        self.assertHttpRespJsonFieldIsTrue(resp, 'status')

        with self.assertRaises(auth.error.InvalidAccessToken):
            auth.get_access_token_info(token)

    def test_get_user(self):
        """GET auth/user
        """
        user = auth.get_user('test_user_1@test.com')
        resp = self.get_user_via_http('test_user_1@test.com')

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldEquals(resp, 'uid', user.uid)

        self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
        self.assertHttpRespJsonFieldIsEmail(resp, 'login')
        self.assertHttpRespJsonFieldIsEmail(resp, 'email')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'last_sign_in')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'last_activity')
        self.assertHttpRespJsonFieldIsInt(resp, 'sign_in_count')
        self.assertHttpRespJsonFieldEquals(resp, 'status', 'active')
        self.assertHttpRespJsonFieldIsBool(resp, 'profile_is_public')
        self.assertHttpRespJsonFieldIsList(resp, 'roles')
        self.assertHttpRespJsonFieldIsUrl(resp, 'profile_url')
        self.assertHttpRespJsonFieldIsList(resp, 'follows')
        self.assertHttpRespJsonFieldIsInt(resp, 'follows_count')
        self.assertHttpRespJsonFieldIsList(resp, 'followers')
        self.assertHttpRespJsonFieldIsInt(resp, 'followers_count')
        self.assertHttpRespJsonFieldIsDict(resp, 'picture')

        self.assertHttpRespJsonFieldEquals(resp, 'nickname', 'nickname-1')
        self.assertHttpRespJsonFieldEquals(resp, 'first_name', 'first_name_1')
        self.assertHttpRespJsonFieldEquals(resp, 'last_name', 'last_name_1')
        self.assertHttpRespJsonFieldEquals(resp, 'full_name', 'first_name_1 last_name_1')
        self.assertHttpRespJsonFieldEquals(resp, 'birth_date', util.w3c_datetime_str(datetime(1984, 7, 1, 1, 1, 1)))
        self.assertHttpRespJsonFieldEquals(resp, 'gender', 'm')
        self.assertHttpRespJsonFieldEquals(resp, 'phone', '+38012345671')
        self.assertHttpRespJsonFieldEquals(resp, 'urls', ['http://test.com/user-1'])

    def test_patch_user(self):
        """PATCH auth/user
        """
        user = auth.get_user('test_user_1@test.com')
        token = auth.generate_access_token(user)

        url = http_api.url('pytsite.auth@patch_user', {'uid': user.uid})
        resp = self.send_http_request(self.prepare_http_request('PATCH', url, {'PytSite-Auth': token}, {
            'nickname': 'new-nickname-1',
            'first_name': 'new_first_name_1',
            'last_name': 'new_last_name_1',
            'birth_date': util.w3c_datetime_str(datetime(2017, 6, 20, 13, 44, 0)),
            'gender': 'f',
            'phone': '+17654321083',
            'urls': json.dumps(['http://test.com/new-user-1']),
        }))
        self.assertHttpRespCodeEquals(resp, 200)

        # Fetch updated user via HTTP
        resp = self.get_user_via_http('test_user_1@test.com')
        self.assertHttpRespCodeEquals(resp, 200)

        updated_user_data = resp.json()
        self.assertEqual(updated_user_data['nickname'], 'new-nickname-1')
        self.assertEqual(updated_user_data['first_name'], 'new_first_name_1')
        self.assertEqual(updated_user_data['last_name'], 'new_last_name_1')
        self.assertEqual(updated_user_data['full_name'], 'new_first_name_1 new_last_name_1')
        self.assertEqual(updated_user_data['birth_date'], util.w3c_datetime_str(datetime(2017, 6, 20, 13, 44, 0)))
        self.assertEqual(updated_user_data['gender'], 'f')
        self.assertEqual(updated_user_data['phone'], '+17654321083')
        self.assertEqual(updated_user_data['urls'], ['http://test.com/new-user-1'])

    def test_post_follow(self):
        user1 = auth.get_user('test_user_1@test.com')
        user2 = auth.get_user('test_user_2@test.com')
        user1_token = auth.generate_access_token(user1)

        url = http_api.url('pytsite.auth@post_follow', {'uid': user2.uid})
        resp = self.send_http_request(self.prepare_http_request('POST', url, {'PytSite-Auth': user1_token}))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsList(resp, 'follows')
        self.assertHttpRespJsonFieldNotEmpty(resp, 'follows')

    def test_delete_follow(self):
        user1 = auth.get_user('test_user_1@test.com')
        user2 = auth.get_user('test_user_2@test.com')
        user1_token = auth.generate_access_token(user1)

        user1.add_follows(user2)

        url = http_api.url('pytsite.auth@delete_follow', {'uid': user2.uid})
        resp = self.send_http_request(self.prepare_http_request('DELETE', url, {'PytSite-Auth': user1_token}))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsList(resp, 'follows')
        self.assertHttpRespJsonFieldIsEmpty(resp, 'follows')
