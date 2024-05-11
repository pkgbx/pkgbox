"""
The cli module is used to run the pkgbox main cli.
"""
import os
import re
import sys
import shutil
import pathlib
from typing import Any

import click

from . import containerfile, errors, env, image, io, runtime


class SourceType(click.ParamType):
    """
    Source type to guess the source uri
    """
    name: str = 'SourceType'

    def convert(self, value: Any, param: click.Parameter, ctx: click.Context) -> io.Reader:
        """
        Converts a source string, such as file:///tmp/Containerfile into reader
        object.

        Supported schemes:

        - file://
        - http(s)://

        "file://" is assumed if no scheme is provided.
        """
        pattern = re.compile('([a-zA-Z]+)//(.*)')
        m = pattern.match(value)
        if m:
            scheme, value = m.groups()
        else:
            scheme, value = ('file', value) 

        return io.build_reader(scheme, value)


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
@click.argument('source', type=SourceType())
@click.option('-r', '--runtime', 'runtime_name', default='crun', help='build runtime to use')
def build(source: SourceType, runtime_name: str) -> None:
    """
    Build a new package from a given source.

    Runtime defaults to "crun" if none is provided.
    """
    paths = env.get_pkgbox_dirs()
    data_dir = paths['data_dir']

    # load containerfile from source
    c = containerfile.from_reader(source)
    click.echo(containerfile.as_json(c, pretty=True))

    # runtime setup
    r = runtime.build(runtime_name)
    r.preflight_check()
    r.prepare_build(containerfile.as_dict(c))
    
    # img = image.from_str(image_name)
    # manifest = image.info(img)
    # dest = pathlib.Path(f'{data_dir}/oci-layers')

    # click.echo(f'Fetching data from "{image_name}"...')
    # image.fetch(img, manifest, dest)
    # click.echo(f'Data fetched into {dest}')


def main() -> None:
    try:
        cli()
    except errors.PBError as e:
        click.echo(str(e), err=True)
        sys.exit(e.errno)
