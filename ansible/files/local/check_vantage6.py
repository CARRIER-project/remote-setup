import click
from vantage6.client import Client


@click.option('--host', prompt=True)
@click.option('--port', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
@click.option('--image', prompt=True)
@click.command()
def check_vantage6(host, port, username, password, image):
    client = Client(host=host, port=port)
    client.authenticate(username, password)

    client.post_task('column_names', image, )