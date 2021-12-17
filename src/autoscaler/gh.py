'''
Logic for handling authentication with Github Actions
'''

from github import Github
import requests


class Runner:
    '''
    Use a personal access token to connect to the Github API

    Args:
        pat: A Personal Access Token string
    '''

    def __init__(
        self,
        pat: str,
        api_url: str = 'https://api.github.com'
    ) -> None:
        self._pat = pat
        self._api = Github(pat)
        self._api_url = api_url


    def _post(
        self,
        suffix: str,
    ):
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self._pat}'
        }

        res = requests.post(self._api_url + suffix, headers=headers)

        if res.status_code >= 300:
            raise ValueError('Something went wrong in the API call')

        return res.json()


    def create_runner_token(
        self,
        user: str,
        repository: str,
    ) -> str:
        '''
        Given a user and a repository that the given token
        is able to authenticate with, create a new repo
        self-hosted runner token

        Args:
            user: the username of the github user
            repository: the repository this will be created for
        '''

        suffix = f'/repos/{user}/{repository}/actions/runners/registration-token'

        token = self._post(suffix)['token']

        return token
