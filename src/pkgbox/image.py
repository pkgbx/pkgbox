import os
import pathlib
from dataclasses import dataclass
from typing import Any, Dict

import requests

from .oci.v1 import Descriptor, Manifest


@dataclass
class Image:
    """
    Image dataclass to store an image reference data
    from an image name, such as "registry.fedoraproject.org/fedora:39".
    """
    registry: str
    namespace: str
    tag: str

    def __str__(self) -> str:
        return f'{self.registry}/{self.namespace}:{self.tag}'

    def __eq__(other: 'Image', self) -> bool:
        if self.registry != other.registry:
            return False

        if self.namespace != other.namespace:
            return False

        if self.tag != other.tag:
            return False

        return True


def from_str(name: str) -> Image:
    """
    Parses an image name string into an Image dataclass instance.
    """
    parts = name.split('/')

    reg = parts[0]
    namespace, tag = '/'.join(parts[1:]).split(':')

    return Image(reg, namespace, tag)


def info(image: Image) -> Manifest:
    """
    Get the required info, such as  layer urls,
    to be fetched.
    """
    baseurl = f'https://{image.registry}/v2/{image.namespace}'

    res = requests.get(f'{baseurl}/manifests/{image.tag}')
    data = res.json()

    return Manifest(
        name=data['name'],
        tag=data['tag'],
        architecture=data['architecture'],
        layers=[Descriptor.from_str(s['blobSum']) for s in data['fsLayers']],
        history=data.get('history', []),
        signatures=data.get('signatures', []),
        digest=Descriptor.from_str(res.headers['docker-content-digest'])
    )


def layer_exists(layer: Descriptor, dest: pathlib.Path) -> bool:
    """
    Checks if a layer exists in dest.
    """
    return os.path.exists(f'{dest}/{layer.digest}.tar.gz')


def fetch(image: Image, manifest: Manifest, dest: pathlib.Path) -> None:
    """
    Fecthes the image and its layers into the `dest` folder.

    `dest` will be created in case it does not exist.
    """
    baseurl = f'https://{image.registry}/v2/{image.namespace}'
    os.makedirs(str(dest), exist_ok=True)

    for layer in manifest.layers:
        if layer_exists(layer, dest):
            continue
        with requests.get(f'{baseurl}/blobs/{layer}', allow_redirects=True, stream=True) as stream:
            stream.raise_for_status()
            with open(f'{dest}/{layer.digest}.tar.gz', 'wb') as f:
                for chunk in stream.iter_content(chunk_size=8192):
                    f.write(chunk)
