"""
"""
from os import path
from pytsite import unittest, auth, http_api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class HttpApiTest(unittest.TestCase):
    def test_post_get(self):
        headers = {'PytSite-Auth': auth.generate_access_token(auth.get_user('user1@test.com'))}

        url = http_api.url('pytsite.file@post')
        f = open(__file__, 'rb')
        files = {'file': (path.basename(__file__), f)}
        resp = self.send_http_request(self.prepare_http_request('POST', url, headers, files=files))
        f.close()

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonIsList(resp)
        self.assertHttpRespJsonIsNotEmpty(resp)
        self.assertDictFieldIsStr(resp.json()[0], 'uid')
        self.assertDictFieldNotEmpty(resp.json()[0], 'uid')

        url = http_api.url('pytsite.file@get', {'uid': resp.json()[0]['uid']})
        resp = self.send_http_request(self.prepare_http_request('get', url, headers))

        self.assertHttpRespCodeEquals(resp, 200)
        self.assertHttpRespJsonFieldIsStr(resp, 'uid')
        self.assertHttpRespJsonFieldNotEmpty(resp, 'uid')
        self.assertHttpRespJsonFieldIsStr(resp, 'description')
        self.assertHttpRespJsonFieldNotEmpty(resp, 'description')
        self.assertHttpRespJsonFieldEquals(resp, 'name', path.basename(__file__))
        self.assertHttpRespJsonFieldEquals(resp, 'mime', 'text/plain')
        self.assertHttpRespJsonFieldIsInt(resp, 'length')
