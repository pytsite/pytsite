"""PytSite Testing Test Case
"""
import re as _re
import requests as _requests
from unittest import TestCase as _TestCase
from pytsite import validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestCase(_TestCase):
    @staticmethod
    def prepare_http_request(method: str, url: str, headers: dict = None, data: dict = None,
                             params: dict = None, files: dict = None) -> _requests.PreparedRequest:
        return _requests.Request(method, url, headers, files, data, params).prepare()

    @staticmethod
    def send_http_request(request: _requests.PreparedRequest):
        with _requests.Session() as s:
            r = s.send(request)

        return r

    def _raiseHttpException(self, msg: str, req: _requests.PreparedRequest = None, resp: _requests.Response = None):
        msg += '\n'

        if req is not None:
            msg += 'Request method: {}\n'.format(req.method)
            msg += 'Request URL: {}\n'.format(req.url)
            msg += 'Request headers: {}\n'.format(req.headers)
            msg += 'Request body: {}\n'.format(req.body)

        if resp is not None:
            msg += 'Response code: {}\n'.format(resp.status_code)
            msg += 'Response headers: {}\n'.format(resp.headers)
            msg += 'Response content: {}\n'.format(resp.content)

        raise self.failureException(msg)

    def assertIsDict(self, d: dict):
        if not isinstance(d, dict):
            raise self.failureException("{} is not a dict".format(d))

    def assertDictContainsField(self, d: dict, key: str):
        self.assertIsDict(d)

        if key not in d:
            raise self.failureException("Dictionary does not contain field '{}'".format(key))

    def assertDictFieldNotEmpty(self, d: dict, key: str):
        self.assertDictContainsField(d, key)

        if not d[key]:
            raise self.failureException("Dictionary field '{}' is empty".format(key))

    def assertDictFieldIsInt(self, d: dict, key: str):
        self.assertDictContainsField(d, key)

        if not isinstance(d[key], int):
            raise self.failureException("Dictionary field '{}' is not an integer".format(key))

    def assertDictFieldIsStr(self, d: dict, key: str):
        self.assertDictContainsField(d, key)

        if not isinstance(d[key], str):
            raise self.failureException("Dictionary field '{}' is not a string".format(key))

    def assertHttpRespCodeEquals(self, resp: _requests.Response, expected: int):
        if resp.status_code != expected:
            self._raiseHttpException('HTTP response code {} != {}'.format(resp.status_code, expected), resp=resp)

    def assertHttpRespContentStrEquals(self, resp: _requests.Response, expected: str):
        if str(resp.content) != expected:
            self._raiseHttpException('HTTP response content {} != {}'.format(resp.content, expected), resp=resp)

    def assertHttpRespIsJson(self, resp: _requests.Response):
        if resp.headers.get('Content-Type') != 'application/json':
            self._raiseHttpException('HTTP response is not JSON', resp=resp)

    def assertHttpRespJsonIsNotEmpty(self, resp: _requests.Response):
        self.assertHttpRespIsJson(resp)

        if not resp.json():
            self._raiseHttpException('HTTP response JSON is empty', resp=resp)

    def assertHttpRespJsonIsList(self, resp: _requests.Response):
        self.assertHttpRespIsJson(resp)

        if not isinstance(resp.json(), list):
            self._raiseHttpException('HTTP response JSON is not a list', resp=resp)

    def assertHttpRespJsonIsDict(self, resp: _requests.Response):
        self.assertHttpRespIsJson(resp)

        if not isinstance(resp.json(), dict):
            self._raiseHttpException('HTTP response JSON is not a dict', resp=resp)

    def assertHttpRespJsonHasField(self, resp: _requests.Response, expected: str):
        self.assertHttpRespJsonIsDict(resp)

        if expected not in resp.json():
            self._raiseHttpException("HTTP response JSON does not contain key '{}'".format(expected), resp=resp)

    def assertHttpRespJsonFieldIsEmpty(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if resp.json()[key]:
            self._raiseHttpException("HTTP response JSON field '{}' is not empty".format(key), resp=resp)

    def assertHttpRespJsonFieldNotEmpty(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not resp.json()[key]:
            self._raiseHttpException("HTTP response JSON field '{}' is empty".format(key), resp=resp)

    def assertHttpRespJsonFieldIsTrue(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if resp.json()[key] is not True:
            self._raiseHttpException("HTTP response JSON field '{}' is not True".format(key), resp=resp)

    def assertHttpRespJsonFieldIsFalse(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if resp.json()[key] is not False:
            self._raiseHttpException("HTTP response JSON field '{}' is not False".format(key), resp=resp)

    def assertHttpRespJsonFieldIsBool(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not isinstance(resp.json()[key], bool):
            self._raiseHttpException("HTTP response JSON field '{}' is not a bool".format(key), resp=resp)

    def assertHttpRespJsonFieldIsInt(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not isinstance(resp.json()[key], int):
            self._raiseHttpException("HTTP response JSON field '{}' is not an integer".format(key), resp=resp)

    def assertHttpRespJsonFieldIsStr(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not isinstance(resp.json()[key], str):
            self._raiseHttpException("HTTP response JSON field '{}' is not a string".format(key), resp=resp)

    def assertHttpRespJsonFieldIsNonEmptyStr(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonFieldIsStr(resp, key)

        if not resp.json()[key]:
            self._raiseHttpException("HTTP response JSON field '{}' is empty string".format(key), resp=resp)

    def assertHttpRespJsonFieldIsList(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not isinstance(resp.json()[key], list):
            self._raiseHttpException("HTTP response JSON field '{}' is not a list".format(key), resp=resp)

    def assertHttpRespJsonFieldListLen(self, resp: _requests.Response, key: str, length: int):
        self.assertHttpRespJsonFieldIsList(resp, key)

        if len(resp.json()[key]) != length:
            self._raiseHttpException("HTTP response JSON field '{}' length != {}".format(key, length), resp=resp)

    def assertHttpRespJsonFieldIsDict(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not isinstance(resp.json()[key], dict):
            self._raiseHttpException("HTTP response JSON field '{}' is not a dict".format(key), resp=resp)

    def assertHttpRespJsonFieldIsNonEmptyDict(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonFieldIsDict(resp, key)

        if not resp.json()[key]:
            self._raiseHttpException("HTTP response JSON field '{}' is empty dict".format(key), resp=resp)

    def assertHttpRespJsonFieldIsDateTime(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        try:
            _validation.rule.DateTime(resp.json()[key]).validate()
        except _validation.error.RuleError:
            if not isinstance(resp.json()[key], int):
                self._raiseHttpException("HTTP response JSON field '{}' is not a valid date".format(key), resp=resp)

    def assertHttpRespJsonFieldIsEmail(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        try:
            _validation.rule.Email(resp.json()[key]).validate()
        except _validation.error.RuleError:
            if not isinstance(resp.json()[key], int):
                self._raiseHttpException("HTTP response JSON field '{}' is not a valid email".format(key), resp=resp)

    def assertHttpRespJsonFieldIsUrl(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        try:
            _validation.rule.Url(resp.json()[key]).validate()
        except _validation.error.RuleError:
            if not isinstance(resp.json()[key], int):
                self._raiseHttpException("HTTP response JSON field '{}' is not a valid URL".format(key), resp=resp)

    def assertHttpRespJsonFieldEquals(self, resp: _requests.Response, key: str, expected):
        self.assertHttpRespJsonHasField(resp, key)

        if resp.json()[key] != expected:
            self._raiseHttpException("HTTP response JSON field '{}' != {}".format(key, expected), resp=resp)

    def assertHttpRespJsonFieldMatches(self, resp: _requests.Response, key: str, expected: str):
        self.assertHttpRespJsonFieldIsStr(resp, key)

        if not _re.match(expected, resp.json()[key]):
            self._raiseHttpException("HTTP response JSON field '{}' does not match pattern '{}'".format(key, expected),
                                     resp=resp)
