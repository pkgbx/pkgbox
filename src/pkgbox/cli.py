"""
The cli module is used to run the pkgbox main cli.
"""
import os
import sys
import shutil
import pathlib

import click

from . import errors, env, image


@click.group
def cli() -> None:
    """
    The main cli group which other subcommands are
    attached to.
    """
    pass

@cli.command
def version() -> None:
    """
    Handles the `pkgbox version` command.
    """
    click.echo('v0.1.0')


@cli.command
def init() -> None:
    """
    Handles the `pkgbox init` command.
    """
    paths = env.get_pkgbox_dirs()

    for k, v in paths.items():
        click.echo(f'{k}: {v}')

    env.ensure_pkgbox_dirs(paths)
    env.bootstrap(paths)


@cli.command
def info() -> None:
    """
    Handles the `pkgbox info` command.
    """
    paths = env.get_pkgbox_dirs()
    
    if not os.path.exists(f'{paths["config_dir"]}/crun/config.json'):
        raise errors.PBError('Pkgbox not intialized. Please run `pkgbox init` first.')

    for k, v in paths.items():
        click.echo(f'{k}: {v}')

    click.echo(f'crun base config: {paths["config_dir"]}/crun/config.json')


@cli.command
@click.option('-i', '--image', 'image_name', default='registry.fedoraproject.org/fedora:39') 
def build(image_name: str) -> None:
    """
    Handles the `pkgbox build` command.
    """
    # paths = env.get_pkgbox_dirs()
    # data_dir = paths['data_dir']
    # img = image.from_str(image_name)
    # manifest = image.info(img)
    # dest = pathlib.Path(f'{data_dir}/oci-layers')

    # click.echo(f'Fetching data from "{image_name}"...')
    # image.fetch(img, manifest, dest)
    # click.echo(f'Data fetched into {dest}')
    raise errors.PBNotImplementedError()


def main() -> None:
    try:
        cli()
    except errors.PBError as e:
        click.echo(str(e), err=True)
        sys.exit(e.errno)
