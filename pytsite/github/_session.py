"""PytSite GitHub Session
"""
import requests as _requests
import re as _re
from pytsite import reg as _reg
from . import _error

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_API_URL = 'https://api.github.com/'

_next_link_re = _re.compile('<(.+?)>; rel="next"')

_error_map = {
    401: _error.Unauthorized,
    403: _error.Forbidden,
    404: _error.NotFound,
}


class Session:
    """PytSite GitHub Session
    """

    def __init__(self, access_token: str = None):
        self._access_token = access_token or _reg.get('github.access_token')

    @staticmethod
    def _request(method: str, url, params: dict = None):
        r = _requests.request(method, url, params=params)

        if r.status_code == 200:
            return r
        elif r.status_code in _error_map:
            raise _error_map[r.status_code]('{} {}: {}'.format(method.upper(), url, r.json()))
        else:
            raise _error.GeneralError('{} {}: {}'.format(method.upper(), url, r.json()))

    def request(self, endpoint: str, method: str = 'get', **kwargs):
        """Make a request to GitHub's API
        """
        params = kwargs
        if self._access_token:
            params.update({
                'access_token': self._access_token,
            })

        return self._request(method, _API_URL + endpoint, params).json()

    def paginated_request(self, endpoint: str, method: str = 'get', per_page: int = 100, **kwargs):
        """Make an automatically paginated request to GitHub's API
        """
        params = kwargs
        params['per_page'] = per_page

        if self._access_token:
            params.update({
                'access_token': self._access_token,
            })

        r = self._request(method, _API_URL + endpoint, params)

        accumulator = r.json()
        while True:
            if 'Link' not in r.headers:
                break

            next_link_found = False
            for h in r.headers['Link'].split(','):
                match = _next_link_re.match(h)
                if match:
                    r = self._request(method, match.group(1))
                    accumulator += r.json()
                    next_link_found = True
                    break

            if not next_link_found:
                break

        return accumulator

    def my_repos(self, visibility: str = 'all', affiliation: str = 'owner,collaborator,organization_member',
                 sort: str = 'full_name', direction: str = 'asc') -> list:
        """List own repositories

        https://developer.github.com/v3/repos/#list-your-repositories
        """
        return self.paginated_request('user/repos', visibility=visibility, affiliation=affiliation, sort=sort,
                                      direction=direction)

    def user_repos(self, user: str, type: str = 'owner', sort: str = 'full_name', direction: str = 'asc') -> list:
        """List user's repositories

        https://developer.github.com/v3/repos/#list-user-repositories
        """
        return self.paginated_request('users/{}/repos'.format(user), type=type, sort=sort, direction=direction)

    def org_repos(self, org: str, type: str = 'all') -> list:
        """List organization's repositories

        https://developer.github.com/v3/repos/#list-organization-repositories
        """
        return self.paginated_request('orgs/{}/repos'.format(org), type=type)

    def repo(self, owner: str, repo: str) -> dict:
        """Get repository's information

        https://developer.github.com/v3/repos/#get
        """
        return self.request('repos/{}/{}'.format(owner, repo))

    def repo_tags(self, owner: str, repo: str) -> list:
        """Get repository's tags

        https://developer.github.com/v3/repos/#list-tags
        """
        return self.paginated_request('repos/{}/{}/tags'.format(owner, repo))

    def repo_contents(self, owner: str, repo: str, path: str, ref: str = 'master') -> dict:
        """Get repository's contents

        https://developer.github.com/v3/repos/contents/#get-contents
        """
        return self.request('repos/{}/{}/contents/{}'.format(owner, repo, path), ref=ref)
