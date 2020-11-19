#!/usr/bin/env python3

from pathlib import Path

from sklearn.datasets import load_diabetes
import pandas as pd
import click

DEFAULT_PATH = Path.cwd() / 'diabetes.csv'


@click.command()
@click.option('--target', type=Path, help='File location for csv file', default=DEFAULT_PATH)
def load_data(target: Path) -> None:
    click.echo('Downloading sample dataset...')
    data = load_diabetes()
    click.echo('Done')

    df = pd.DataFrame(data=data.data, columns=data.feature_names)

    click.echo(f'Storing data in {str(target)}')
    df.to_csv(target, index=False)
    click.echo('Done')


if __name__ == '__main__':
    load_data()
