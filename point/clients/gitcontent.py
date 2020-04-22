import requests
import logging

LOG = logging.getLogger(__name__)
API_BASE = 'https://api.github.com'


class GitContent:
    def __init__(self, token=None):
        self.token = token

    def headers(self):
        return {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3.raw'
        }

    def get(self, owner, repo, path):
        uri = '/'.join((API_BASE, 'repos', owner, repo, 'contents', path))
        LOG.info(uri)
        LOG.info(self.headers())
        response = requests.get(uri, headers=self.headers())
        # TODO if 200
        return response.text


if __name__ == '__main__':
    content = GitContent('547aab467888465fd508cc065105a31e5aabc7fc').get('trevorgrayson', 'private', 'example.dot')
    print(content)