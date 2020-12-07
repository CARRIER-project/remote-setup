import click
from vantage6.client import Client


@click.option('--host')
@click.option('--port', type=int)
@click.option('--username')
@click.option('--password')
@click.option('--image')
@click.command()
def check_vantage6(host, port, username, password, image):
    host = f'https://{host}'
    client = Client(host=host, port=port)
    client.authenticate(username, password)
    client.setup_encryption(None)

    organization = client.whoami.organization_id
    collaboration_id = client.request(f'organization/{organization}/collaboration')
    collaboration_id = collaboration_id['id']

    task = client.post_task('column_names', image, collaboration_id)

    print(task)


def main():
    check_vantage6()


if __name__ == '__main__':
    main()
