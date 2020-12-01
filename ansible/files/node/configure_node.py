#!/usr/bin/env python3

import click

from VantageClient import VantageClient


LOCALHOST = 'localhost'
DEFAULT_PORT = 5000




USERNAME = 'root'
PASSWORD = 'root'
ADMIN_PASSWORD = 'admin'
COLLABORATION_ID = 1

ORGANIZATION_BASE = ORGANIZATION = {'address1': 'my address 1, Amsterdam',
                                    'country': 'the Netherlands',
                                    'zipcode': '1234ab'}


@click.command()
@click.argument('name')
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
@click.option('--host', default='localhost', prompt=True)
@click.option('--port', default=DEFAULT_PORT, prompt=True)
def create_node(name, username, password, host, port):
    client = VantageClient(username, password, host, port)

    click.echo('Creating new organization')
    org_id = create_organization(client, name)

    create_user(client, org_id, username)

    # Create node
    client = VantageClient(username, password)
    result = client.post('node', {'collaboration_id': COLLABORATION_ID, 'organization_id': org_id})

    click.echo(result)


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
    click.echo(f'Created new user:\n{result}')


if __name__ == '__main__':
    create_node()


