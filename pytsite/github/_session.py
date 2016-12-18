"""PytSite GitHub API Functions.
"""
import requests as _requests
from pytsite import reg as _reg
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_API_URL = 'https://api.github.com/'


class Session:
    def __init__(self, access_token: str = None):
        self._access_token = access_token or _reg.get('github.access_token')

    def request(self, endpoint: str, method: str = 'get', **kwargs):
        """Make a request to the GitHub API.
        """
        url = _API_URL + endpoint
        params = kwargs

        if self._access_token:
            params.update({
                'access_token': self._access_token,
            })

        r = _requests.request(method, url, params=params)

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise _error.Unauthorized('{} {}: {}'.format(method.upper(), url, r.json()))
        elif r.status_code == 403:
            raise _error.Forbidden('{} {}: {}'.format(method.upper(), url, r.json()))
        elif r.status_code == 404:
            raise _error.NotFound('{} {}: {}'.format(method.upper(), url, r.json()))
        else:
            raise _error.GeneralError('{} {}: {}'.format(method.upper(), url, r.json()))

    def my_repos(self, visibility: str = 'all', affiliation: str = 'owner,collaborator,organization_member',
                 sort: str = 'full_name', direction: str = 'asc') -> list:
        """List your repositories.

        https://developer.github.com/v3/repos/#list-your-repositories
        """
        return self.request('user/repos', visibility=visibility, affiliation=affiliation, sort=sort,
                            direction=direction)

    def user_repos(self, user: str, type: str = 'owner', sort: str = 'full_name', direction: str = 'asc') -> list:
        """List user repositories.

        https://developer.github.com/v3/repos/#list-user-repositories
        """
        return self.request('users/{}/repos'.format(user), type=type, sort=sort, direction=direction)

    def org_repos(self, org: str, type: str = 'all') -> list:
        """List organization repositories.

        https://developer.github.com/v3/repos/#list-organization-repositories
        """
        return self.request('orgs/{}/repos'.format(org), type=type)

    def repo(self, owner: str, repo: str) -> dict:
        """Get repository information.

        https://developer.github.com/v3/repos/#get
        """
        return self.request('repos/{}/{}'.format(owner, repo))

    def repo_tags(self, owner: str, repo: str) -> list:
        """Get repository tags.

        https://developer.github.com/v3/repos/#list-tags
        """
        return self.request('repos/{}/{}/tags'.format(owner, repo))

    def repo_contents(self, owner: str, repo: str, path: str) -> dict:
        """Get repository contents.

        https://developer.github.com/v3/repos/contents/#get-contents
        """
        return self.request('repos/{}/{}/contents/{}'.format(owner, repo, path))
