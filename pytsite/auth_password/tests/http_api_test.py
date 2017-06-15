"""
"""
from pytsite import testing, http_api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestHttpApi(testing.TestCase):
    def test_post_access_token(self):
        url = http_api.url('pytsite.auth@post_access_token', {'driver': 'password'})
        resp = self.send_http_request(self.prepare_http_request('POST', url, data={
            'login': 'user1@test.com',
            'password': 'user1',
        }))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsDateTime(resp, 'created')
        self.assertHttpRespJsonFieldIsDateTime(resp, 'expires')
        self.assertHttpRespJsonFieldNotEmpty(resp, 'user_uid')
        self.assertHttpRespJsonFieldIsInt(resp, 'ttl')
        self.assertHttpRespJsonFieldMatches(resp, 'token', '^[0-9a-f]{32}$')
