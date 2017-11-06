"""PytSite Auth HTTP API Tests
"""
import json
from typing import List
from datetime import datetime
from random import randint as _randint
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
        self.users = []  # type: List[auth.model.AbstractUser]
        auth.switch_user_to_system()

        # Create test users
        for i in range(3):
            user = auth.create_user('test_user_{}@test.com'.format(i), 'test_user_{}_password'.format(i))
            user.set_field('nickname', 'nickname-{}'.format(i))
            user.set_field('first_name', 'first_name_{}'.format(i))
            user.set_field('last_name', 'last_name_{}'.format(i))
            user.set_field('description', 'description_{}'.format(i))
            user.set_field('birth_date', datetime(1984, 7, i + 1, i, i, i))
            user.set_field('gender', 'm' if i in (1, 3) else 'f')
            user.set_field('phone', '+3801234567{}'.format(i))
            user.set_field('urls', ['http://test.com/user-{}'.format(i)])
            user.set_field('country', 'Ukraine')
            user.set_field('city', 'Kyiv')
            user.set_field('profile_is_public', True if i in (1, 3) else False)
            user.save()

            self.users.append(user)

        auth.restore_user()

    def tearDown(self):
        """Tear down
        """
        auth.switch_user_to_system()

        # Delete created test users
        for user in self.users:
            user.delete()

        self.users = []

        auth.restore_user()

    def _get_user_via_http(self, login: str, version, requester_login: str = None):
        """Helper
        """
        url = http_api.url('pytsite.auth@get_user', {'uid': auth.get_user(login).uid}, version)

        if requester_login:
            token = auth.generate_access_token(auth.get_user(requester_login))
            return self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': token}))
        else:
            return self.send_http_request(self.prepare_http_request('GET', url))

    def _check_http_user_response(self):
        pass

    def test_post_access_token(self):
        """
        POST auth/access_token/:driver

        There is no code because it should be implemented by authentication drivers
        """
        pass

    def test_get_access_token(self):
        """
        GET auth/access-token/:token
        """
        for version in (1, 2):
            for user in self.users:
                token = auth.generate_access_token(user)
                url = http_api.url('pytsite.auth@get_access_token', {'token': token}, version)
                resp = self.send_http_request(self.prepare_http_request('GET', url))

                self.assertHttpRespCodeEquals(resp, 200)
                self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
                self.assertHttpRespJsonFieldIsDateTime(resp, 'expires')
                self.assertHttpRespJsonFieldNotEmpty(resp, 'user_uid')
                self.assertHttpRespJsonFieldIsInt(resp, 'ttl')
                self.assertHttpRespJsonFieldEquals(resp, 'token', token)

    def test_delete_access_token(self):
        """
        DELETE auth/access-token/:token
        """
        for version in (1, 2):
            for user in self.users:
                token = auth.generate_access_token(user)
                url = http_api.url('pytsite.auth@delete_access_token', {'token': token}, version)
                resp = self.send_http_request(self.prepare_http_request('DELETE', url))
                self.assertHttpRespJsonFieldIsTrue(resp, 'status')

                with self.assertRaises(auth.error.InvalidAccessToken):
                    auth.get_access_token_info(token)

    def test_is_anonymous(self):
        """
        GET auth/is_anonymous
        """
        for version in (1, 2):
            # Anonymous request
            req = self.prepare_http_request('GET', http_api.url('pytsite.auth@is_anonymous', version=version))
            res = self.send_http_request(req)
            if version == 1:
                self.assertHttpRespContentStrEquals(res, 'true')
            else:
                self.assertHttpRespJsonFieldIsTrue(res, 'status')

            # Authenticated requests
            for user in self.users:
                token = auth.generate_access_token(user)
                url = http_api.url('pytsite.auth@is_anonymous', version=version)
                res = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': token}))
                if version == 1:
                    self.assertHttpRespContentStrEquals(res, 'false')
                else:
                    self.assertHttpRespJsonFieldIsFalse(res, 'status')

    def test_get_user(self):
        """
        GET auth/user/:uid
        """
        i = _randint(1, 2)
        user = self.users[i]
        b_date = util.w3c_datetime_str(datetime(1984, 7, i + 1, i, i, i))

        for version in (1, 2):
            for requester_login in (None, 'test_user_1@test.com', user.login):
                resp = self._get_user_via_http('test_user_{}@test.com'.format(i), version, requester_login)

                self.assertHttpRespCodeEquals(resp, 200)
                self.assertHttpRespJsonFieldEquals(resp, 'uid', user.uid)

                # Requester is authenticated user, but not a current user, profile is public
                if requester_login != user.login and user.profile_is_public:
                    self.assertHttpRespJsonFieldIsUrl(resp, 'profile_url')
                    self.assertHttpRespJsonFieldEquals(resp, 'nickname', 'nickname-{}'.format(i))
                    self.assertHttpRespJsonFieldIsDict(resp, 'picture')
                    self.assertHttpRespJsonFieldEquals(resp, 'first_name', 'first_name_{}'.format(i))
                    self.assertHttpRespJsonFieldEquals(resp, 'last_name', 'last_name_{}'.format(i))
                    self.assertHttpRespJsonFieldEquals(resp, 'full_name', 'first_name_{} last_name_{}'.format(i, i))
                    self.assertHttpRespJsonFieldEquals(resp, 'birth_date', b_date)
                    self.assertHttpRespJsonFieldEquals(resp, 'gender', 'm' if i in (1, 3) else 'f')
                    self.assertHttpRespJsonFieldEquals(resp, 'phone', '+3801234567{}'.format(i))
                    self.assertHttpRespJsonFieldEquals(resp, 'urls', ['http://test.com/user-{}'.format(i)])

                    # Following fields are present only in version 1
                    if version == 1:
                        self.assertHttpRespJsonFieldIsList(resp, 'follows')
                        self.assertHttpRespJsonFieldIsInt(resp, 'follows_count')
                        self.assertHttpRespJsonFieldIsList(resp, 'followers')
                        self.assertHttpRespJsonFieldIsInt(resp, 'followers_count')
                        self.assertHttpRespJsonFieldIsBool(resp, 'is_followed')
                        self.assertHttpRespJsonFieldIsBool(resp, 'is_follows')

                # Requester is authenticated and it is the same user
                elif requester_login == user.login:
                    self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
                    self.assertHttpRespJsonFieldEquals(resp, 'login', 'test_user_{}@test.com'.format(i))
                    self.assertHttpRespJsonFieldEquals(resp, 'email', 'test_user_{}@test.com'.format(i))
                    self.assertHttpRespJsonFieldIsDateTime(resp, 'last_sign_in')
                    self.assertHttpRespJsonFieldIsDateTime(resp, 'last_activity')
                    self.assertHttpRespJsonFieldIsInt(resp, 'sign_in_count')
                    self.assertHttpRespJsonFieldEquals(resp, 'status', 'active')
                    self.assertHttpRespJsonFieldIsBool(resp, 'profile_is_public')
                    self.assertHttpRespJsonFieldIsList(resp, 'roles')

                    # Following fields are present only in version 1
                    if version == 1:
                        self.assertHttpRespJsonFieldIsList(resp, 'blocked_users')

                # Anonymous requester and requested profile is not public
                else:
                    self.assertHttpRespJsonDictLen(resp, 1)

    def test_get_users(self):
        """
        GET auth/users
        """
        users_uids = [u.uid for u in self.users]
        for version in (1, 2):
            url = http_api.url('pytsite.auth@get_users', {'uids': users_uids}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url))
            self.assertHttpRespCodeEquals(resp, 200)
            self.assertHttpRespJsonListLen(resp, len(self.users))

    def test_patch_user(self):
        """
        PATCH auth/user/:uid
        """
        i = _randint(0, 2)
        user = self.users[i]  # type: auth.model.AbstractUser
        token = auth.generate_access_token(user)
        birth_date = datetime(2017, 6, 20, 13, 44, 0)

        url = http_api.url('pytsite.auth@patch_user', {'uid': user.uid})
        resp = self.send_http_request(self.prepare_http_request('PATCH', url, {'PytSite-Auth': token}, {
            'nickname': 'new-nickname-{}'.format(i),
            'first_name': 'new_first_name_{}'.format(i),
            'last_name': 'new_last_name_{}'.format(i),
            'birth_date': util.w3c_datetime_str(birth_date),
            'gender': 'f',
            'phone': '+17654321083',
            'urls': json.dumps(['http://test.com/new-user-{}'.format(i)]),
        }))
        self.assertHttpRespCodeEquals(resp, 200)

        user = auth.get_user(user.login)
        self.assertEqual(user.nickname, 'new-nickname-{}'.format(i))
        self.assertEqual(user.first_name, 'new_first_name_{}'.format(i))
        self.assertEqual(user.last_name, 'new_last_name_{}'.format(i))
        self.assertEqual(user.full_name, 'new_first_name_{} new_last_name_{}'.format(i, i))
        self.assertEqual(user.birth_date, birth_date)
        self.assertEqual(user.gender, 'f')
        self.assertEqual(user.phone, '+17654321083')
        self.assertEqual(user.urls, ('http://test.com/new-user-{}'.format(i),))

    def test_post_follow_delete_follow(self):
        """
        POST auth/follow/:uid
        DELETE auth/follow/:uid
        """
        user1 = self.users[0]  # type: auth.model.AbstractUser
        user2 = self.users[1]  # type: auth.model.AbstractUser
        user1_token = auth.generate_access_token(user1)

        for version in (1, 2):
            self.assertEqual(user1.follows, [])
            self.assertEqual(user2.followers, [])
            self.assertEqual(user1.follows_count, 0)
            self.assertEqual(user2.followers_count, 0)

            # Follow
            url = http_api.url('pytsite.auth@post_follow', {'uid': user2.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('POST', url, {'PytSite-Auth': user1_token}))
            self.assertHttpRespCodeEquals(resp, 200)
            if version == 1:
                self.assertHttpRespJsonFieldEquals(resp, 'follows', [user2.uid])
            else:
                self.assertHttpRespJsonFieldEquals(resp, 'status', True)
            self.assertEqual(user1.follows, [user2])
            self.assertEqual(user2.followers, [user1])
            self.assertEqual(user1.follows_count, 1)
            self.assertEqual(user2.followers_count, 1)

            # Unfollow
            url = http_api.url('pytsite.auth@delete_follow', {'uid': user2.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('DELETE', url, {'PytSite-Auth': user1_token}))
            self.assertHttpRespCodeEquals(resp, 200)
            if version == 1:
                self.assertHttpRespJsonFieldIsList(resp, 'follows')
                self.assertHttpRespJsonFieldIsEmpty(resp, 'follows')
            else:
                self.assertHttpRespJsonFieldEquals(resp, 'status', True)
            self.assertEqual(user1.follows, [])
            self.assertEqual(user2.followers, [])
            self.assertEqual(user1.follows_count, 0)
            self.assertEqual(user2.followers_count, 0)

    def test_get_follows_get_followers(self):
        """
        GET auth/follows/:uid
        GET auth/followers/:uid
        """
        user1 = self.users[0]  # type: auth.model.AbstractUser
        user1_token = auth.generate_access_token(user1)

        user2 = self.users[1]  # type: auth.model.AbstractUser
        user2_token = auth.generate_access_token(user2)

        user3 = self.users[2]  # type: auth.model.AbstractUser
        user3_token = auth.generate_access_token(user3)

        for version in (2,):
            # Test addition
            user1.add_follows(user2)
            user1.add_follows(user3)

            # Check follows of user 1 after addition
            url = http_api.url('pytsite.auth@get_follows', {'uid': user1.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user1_token}))
            self.assertHttpRespCodeEquals(resp, 200)
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 2)
            self.assertEqual(resp.json()['result'][0]['uid'], user2.uid)
            self.assertEqual(resp.json()['result'][1]['uid'], user3.uid)

            # Check followers of user 2 addition
            url = http_api.url('pytsite.auth@get_followers', {'uid': user2.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user2_token}))
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 1)
            self.assertEqual(resp.json()['result'][0]['uid'], user1.uid)

            # Check followers of user 3 addition
            url = http_api.url('pytsite.auth@get_followers', {'uid': user3.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user3_token}))
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 1)
            self.assertEqual(resp.json()['result'][0]['uid'], user1.uid)

            # Test deletion
            user1.remove_follows(user2)
            user1.remove_follows(user3)

            # Check follows of user 1 after deletion
            url = http_api.url('pytsite.auth@get_follows', {'uid': user1.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user1_token}))
            self.assertHttpRespCodeEquals(resp, 200)
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 0)

            # Check followers of user 2 after deletion
            url = http_api.url('pytsite.auth@get_followers', {'uid': user2.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user2_token}))
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 0)

            # Check followers of user 3 after deletion
            url = http_api.url('pytsite.auth@get_followers', {'uid': user3.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user3_token}))
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 0)

    def test_get_blocked_users(self):
        user1 = self.users[0]  # type: auth.model.AbstractUser
        user2 = self.users[1]  # type: auth.model.AbstractUser
        user3 = self.users[2]  # type: auth.model.AbstractUser

        user1_token = auth.generate_access_token(user1)

        for version in (2,):
            # Test addition
            user1.add_blocked_user(user2)
            user1.add_blocked_user(user3)
            url = http_api.url('pytsite.auth@get_blocked_users', {'uid': user1.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user1_token}))
            self.assertHttpRespCodeEquals(resp, 200)
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 2)
            self.assertEqual(resp.json()['result'][0]['uid'], user2.uid)
            self.assertEqual(resp.json()['result'][1]['uid'], user3.uid)

            # Test deletion
            user1.remove_blocked_user(user2)
            user1.remove_blocked_user(user3)
            url = http_api.url('pytsite.auth@get_blocked_users', {'uid': user1.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('GET', url, {'PytSite-Auth': user1_token}))
            self.assertHttpRespCodeEquals(resp, 200)
            self.assertHttpRespJsonFieldIsInt(resp, 'remains')
            self.assertHttpRespJsonFieldListLen(resp, 'result', 0)

    def test_post_block_user_delete_block_user(self):
        user1 = self.users[0]  # type: auth.model.AbstractUser
        user2 = self.users[1]  # type: auth.model.AbstractUser
        user1_token = auth.generate_access_token(user1)

        for version in (1, 2):
            # Block
            self.assertEqual(user1.blocked_users, [])
            self.assertEqual(user1.blocked_users_count, 0)
            url = http_api.url('pytsite.auth@post_block_user', {'uid': user2.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('POST', url, {'PytSite-Auth': user1_token}))
            if version == 1:
                self.assertHttpRespJsonFieldEquals(resp, 'blocked_users', [user2.uid])
            else:
                self.assertHttpRespJsonFieldEquals(resp, 'status', True)
            self.assertEqual(user1.blocked_users, [user2])
            self.assertEqual(user1.blocked_users_count, 1)

            # Unblock
            url = http_api.url('pytsite.auth@delete_block_user', {'uid': user2.uid}, version)
            resp = self.send_http_request(self.prepare_http_request('DELETE', url, {'PytSite-Auth': user1_token}))
            if version == 1:
                self.assertHttpRespJsonFieldEquals(resp, 'blocked_users', [])
            else:
                self.assertHttpRespJsonFieldEquals(resp, 'status', True)
            self.assertEqual(user1.blocked_users, [])
            self.assertEqual(user1.blocked_users_count, 0)
