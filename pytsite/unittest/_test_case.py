"""
"""
import re as _re
import requests as _requests
from unittest import TestCase as _TestCase
from pytsite import validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestCase(_TestCase):
    def prepare_http_request(self, method: str, url: str, headers: dict = None, data: dict = None,
                             params: dict = None) -> _requests.PreparedRequest:
        return _requests.Request(method, url, headers, data=data, params=params).prepare()

    def send_http_request(self, request: _requests.PreparedRequest):
        with _requests.Session() as s:
            r = s.send(request)

        return r

    def _raiseHttpException(self, msg: str, req: _requests.PreparedRequest = None, resp: _requests.Response = None):
        msg += '\n'

        if req:
            msg += 'Request method: {}\n'.format(req.method)
            msg += 'Request URL: {}\n'.format(req.url)
            msg += 'Request headers: {}\n'.format(req.headers)
            msg += 'Request body: {}\n'.format(req.body)

        if resp:
            msg += 'Response code: {}\n'.format(resp.status_code)
            msg += 'Response headers: {}\n'.format(resp.headers)
            msg += 'Response content: {}\n'.format(resp.content)

        raise self.failureException(msg)

    def assertHttpRespCodeEquals(self, resp: _requests.Response, expected: int):
        if resp.status_code != expected:
            self._raiseHttpException('HTTP response code {} != {}'.format(resp.status_code, expected), resp=resp)

    def assertHttpRespContentStrEquals(self, resp: _requests.Response, expected: str):
        if str(resp.content) != expected:
            self._raiseHttpException('HTTP response content {} != {}'.format(resp.content, expected), resp=resp)

    def assertHttpRespJsonHasField(self, resp: _requests.Response, expected: str):
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

    def assertHttpRespJsonFieldIsList(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not isinstance(resp.json()[key], list):
            self._raiseHttpException("HTTP response JSON field '{}' is not a list".format(key), resp=resp)

    def assertHttpRespJsonFieldIsDict(self, resp: _requests.Response, key: str):
        self.assertHttpRespJsonHasField(resp, key)

        if not isinstance(resp.json()[key], dict):
            self._raiseHttpException("HTTP response JSON field '{}' is not a dict".format(key), resp=resp)

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
        self.assertHttpRespJsonHasField(resp, key)

        if not _re.match(expected, resp.json()[key]):
            self._raiseHttpException("HTTP response JSON field '{}' does not match pattern '{}'".format(key, expected),
                                     resp=resp)
