"""Tumblr Session.
"""
from requests_oauthlib import OAuth1Session as _OAuthSession
from pytsite import reg as _reg, router as _router, validation as _validation, cache as _cache
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_API_BASE_URL = 'https://api.tumblr.com/v2/'
_request_tokens = _cache.create_pool('pytsite.tumblr.tokens')


class AuthSession:
    def __init__(self, request_token: str=None, callback_uri: str=None):
        self._app_key = _reg.get('tumblr.app_key')
        self._app_secret = _reg.get('tumblr.app_secret')
        self._request_token = None
        self._request_secret = None
        self._oauth_session = None
        self._callback_uri = callback_uri if callback_uri else _router.current_url()

        if request_token:
            if _request_tokens.has(request_token):
                self._request_token = request_token
                self._request_secret = _request_tokens.get(request_token)
                self._oauth_session = _OAuthSession(self._app_key, self._app_secret,
                                                    self._request_token, self._request_secret, self._callback_uri)
            else:
                raise Exception('Cannot find token secret corresponding to the specified token.')

    def fetch_request_token(self):
        if self._oauth_session:
            raise Exception('Request token already fetched.')

        s = _OAuthSession(self._app_key, self._app_secret, callback_uri=self._callback_uri)
        r = s.fetch_request_token('https://tumblr.com/oauth/request_token')

        _request_tokens.put(r['oauth_token'], r['oauth_token_secret'], 60)
        self._request_token = r['oauth_token']
        self._request_secret = r['oauth_token_secret']
        self._oauth_session = _OAuthSession(self._app_key, self._app_secret,
                                            self._request_token, self._request_secret, self._callback_uri)

        return self

    def get_authorization_url(self) -> str:
        if not self._oauth_session:
            raise Exception('fetch_request_token() must be called before this method.')

        return self._oauth_session.authorization_url('https://www.tumblr.com/oauth/authorize')

    def get_access_token(self, authorization_response_url: str) -> dict:
        if not self._oauth_session:
            raise Exception('fetch_request_token() must be called before this method.')
        auth_data = self._oauth_session.parse_authorization_response(authorization_response_url)

        return self._oauth_session.fetch_access_token('https://www.tumblr.com/oauth/access_token',
                                                      auth_data['oauth_verifier'])


class Session:
    def __init__(self, oauth_token: str, oauth_token_secret: str):
        self._client = _OAuthSession(_reg.get('tumblr.app_key'), _reg.get('tumblr.app_secret'),
                                     oauth_token, oauth_token_secret)

    def request(self, endpoint: str, method='GET', **kwargs):
        if method.upper() == 'POST':
            r = self._client.post(_API_BASE_URL + endpoint, data=kwargs)
        else:
            r = self._client.get(_API_BASE_URL + endpoint, data=kwargs)

        r = r.json()
        status = r['meta']['status']
        if status < 200 or status > 299:
            raise _error.RequestError(r)

        return r['response']

    def user_info(self) -> dict:
        return self.request('user/info')['user']

    def blog_request(self, blog: str, ep: str, **kwargs):
        if ep == 'post':
            method = 'POST'
        else:
            method = 'GET'

        return self.request('blog/{}.tumblr.com/{}'.format(blog, ep), method, **kwargs)

    def blog_post_text(self, blog: str, body: str, title: str=None) -> int:
        return self.blog_request(blog, 'post', type='text', body=body, title=title)['id']

    def blog_post_link(self, blog: str, url: str, title: str=None, description: str=None,
                       thumb_url: str=None, excerpt: str=None, author: str=None, tags: str=None) -> int:
        _validation.rule.Url(url).validate()
        return self.blog_request(blog, 'post', type='link', url=url, title=title, description=description,
                                 thumbnail=thumb_url, excerpt=excerpt, author=author, tags=tags)['id']
