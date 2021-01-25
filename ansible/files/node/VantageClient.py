import json

import click
import requests

DEFAULT_CONTENT_TYPE = 'application/json'
PREFIX = 'api'
DEFAULT_HEADERS = {'Content-Type': DEFAULT_CONTENT_TYPE}
OK_RESPONSES = [200, 201]
POST = 'POST'


class NotOkResponse(Exception):
    def __init__(self, status_code):
        super(self)
        self.status_code = status_code


class VantageClient:
    """
    Custom made vantage client to work around some problems the official has at the moment (such as authenticating root
    users).
    """

    def __init__(self, username, password, host, port):
        self.host = host
        self.port = port

        # Retrieve a authentication token
        self.token = self.get_token(username, password)
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': DEFAULT_CONTENT_TYPE
        }

    def get_server_root(self):
        return f'{self.host}:{self.port}/{PREFIX}/'

    def get_url(self, endpoint) -> str:
        return 'http://' + self.get_server_root() + endpoint

    def get_token(self, username, password):
        result = self.request('token/user', {'username': username, 'password': password}, headers=DEFAULT_HEADERS,
                              method=POST)
        return result['access_token']

    def get(self, endpoint, payload=None, headers=None) -> dict:
        return self.request(endpoint, payload, headers, 'GET')

    def post(self, endpoint, payload, headers=None):
        click.echo(f'Posting: {payload}')
        return self.request(endpoint, payload, headers, 'POST')

    # def post_task(self, name, image, collaboration_id, organizations):
    #     for o in organizations:
    #         input_base64 = base64.b64encode(pickle.dumps(o['input']))
    #         o['input'] = str(input_base64, 'utf8')
    #         click.echo(f'Base64 converted input: {o}')
    #
    #     payload = {'collaboration_id': collaboration_id, 'image': image, 'name': name, 'organizations': organizations}
    #     return self.post('task', payload)

    def request(self, endpoint, payload, headers=None, method='GET') -> dict:
        if headers is None:
            headers = self.headers

        url = self.get_url(endpoint)

        click.echo(f'Request {method} {url}')

        headers['Content-Type'] = 'application/json'
        response = requests.request(method, url, headers=headers, data=json.dumps(payload))

        if response.status_code in OK_RESPONSES:
            return response.json()
        else:
            raise NotOkResponse(response.status_code)
