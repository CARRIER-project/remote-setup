#!/usr/bin/env python3

import requests
import click
import json

DEFAULT_CONTENT_TYPE = 'application/json'

DEFAULT_HEADERS = {'Content-Type': DEFAULT_CONTENT_TYPE}
OK_RESPONSES = [200, 201]
HOST = 'localhost'
PORT = 5001
PREFIX = 'api'
DEFAULT_SERVER_ROOT = f'{HOST}:{PORT}/{PREFIX}/'
POST = 'POST'

USERNAME = 'root'
PASSWORD = 'root'
ADMIN_PASSWORD = 'admin'
COLLABORATION_ID = 1

ORGANIZATION_BASE = ORGANIZATION = {'address1': 'my address 1, Amsterdam',
                                    'country': 'the Netherlands',
                                    'zipcode': '1234ab'}


@click.command()
@click.argument('name')
@click.option('--username')
@click.option('--password', default=ADMIN_PASSWORD)
def create_node(name, username, password):
    client = VantageClient(USERNAME, PASSWORD)

    print('Creating new organization')
    org_id = create_organization(client, name)

    create_user(client, org_id, username)

    # Create node
    client = VantageClient(username, password)
    result = client.post('node', {'collaboration_id': COLLABORATION_ID, 'organization_id': org_id})
    api_key = result['api_key']

    print(f'Created new node. Api key: {api_key}')


def create_organization(client, name):
    # Create organization for node
    organization = dict(ORGANIZATION_BASE)
    organization['name'] = name
    result = client.post('organization', organization)
    org_id = result['id']
    return org_id


def create_user(client, organization_id, username):
    user = {'firstname': ' ', 'lastname': ' ', 'username': username, 'organization_id': organization_id,
            'password': ADMIN_PASSWORD, 'roles': ['admin']}
    result = client.post('user', user)
    print(f'Created new user:\n{result}')


if __name__ == '__main__':
    create_node()


class VantageClient:
    """
    Custom made vantage client to work around some problems the official has at the moment (such as authenticating root
    users).
    """

    def __init__(self, username, password):
        # Retrieve a authentication token
        self.token = self.get_token(username, password)
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': DEFAULT_CONTENT_TYPE
        }

    @staticmethod
    def get_url(endpoint) -> str:
        return 'http://' + DEFAULT_SERVER_ROOT + endpoint

    def get_token(self, username, password):
        result = self.request('token/user', {'username': username, 'password': password}, headers=DEFAULT_HEADERS,
                              method=POST)
        return result['access_token']

    def get(self, endpoint, payload=None, headers=None) -> dict:
        return self.request(endpoint, payload, headers, 'GET')

    def post(self, endpoint, payload, headers=None):
        print(f'Posting: {payload}')
        return self.request(endpoint, payload, headers, 'POST')

    # def post_task(self, name, image, collaboration_id, organizations):
    #     for o in organizations:
    #         input_base64 = base64.b64encode(pickle.dumps(o['input']))
    #         o['input'] = str(input_base64, 'utf8')
    #         print(f'Base64 converted input: {o}')
    #
    #     payload = {'collaboration_id': collaboration_id, 'image': image, 'name': name, 'organizations': organizations}
    #     return self.post('task', payload)

    def request(self, endpoint, payload, headers=None, method='GET') -> dict:
        if headers is None:
            headers = self.headers

        url = VantageClient.get_url(endpoint)

        print(f'Request {method} {url}')

        headers['Content-Type'] = 'application/json'
        response = requests.request(method, url, headers=headers, data=json.dumps(payload))

        if response.status_code in OK_RESPONSES:
            return response.json()
        else:
            raise Exception(f'Request returned status {response.status_code}\nMessage: {response.content}')
