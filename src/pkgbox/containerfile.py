"""
This module handles the parsing and management
of Containerfiles content.
"""
import json
import hashlib
import pathlib
from typing import Dict, Any

import canonicaljson
from dockerfile_parse import DockerfileParser, util


class ContainerfileParser(DockerfileParser):
    """
    A class that inherits DockerfileParser to handle
    cached content in a specific way.
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Create a new object instance, forcing the
        parent class parser to used the cached content.
        """
        super().__init__(*args, **kwargs)
        self.cache_content = True

    @property
    def content(self) -> str:
        """
        Overwrites the parent method to return
        the cached content.
        """
        return self.cached_content

    @content.setter
    def content(self, content: str) -> None:
        """
        Overwrites the parent method to not to any file
        operations.
        """
        self.cached_content = util.b2u(content)


def from_filepath(path: pathlib.Path) -> ContainerfileParser:
    """
    Return a parser object from a given path, where path
    should be the location of a Containerfile.
    """
    parser = ContainerfileParser()

    with open(path.resolve(), 'r') as f:
        parser.content = f.read()

    return parser


def as_dict(parser: ContainerfileParser) -> Dict[str, str]:
    """
    Return the dict representation of a ContainerfileParser(DockerfileParser).
    """
    data = {
        'from': parser.baseimage,
        'labels': parser.labels,
        'envs': parser.envs,
        'cmd': parser.cmd, 
        'args': parser.args,
        'build_args': parser.build_args, 
        'instructions': {
            'digest': None,
            'items': [
                {'name': i['instruction'], 'value': i['value'], 'digest': 'sha256:' + digest_instruction(i)}
                for i in parser.structure
            ]
        }
    }

    data['instructions']['digest'] = ''.join([i['digest'].split(':')[1] for i in data['instructions']['items']])
    data['instructions']['digest'] = 'sha256:' + hashlib.sha256(data['instructions']['digest'].encode()).hexdigest()

    return data


def as_json(parser: ContainerfileParser, pretty: bool = False) -> str:
    """
    Return a json string representation of a parsed containerfile.
    """
    if pretty:
        return canonicaljson.encode_pretty_printed_json(as_dict(parser)).decode()    
    return canonicaljson.encode_canonical_json(as_dict(parser)).decode()


def digest_instruction(data: Dict[str, str]) -> str:
    """
    Return the sha256 string represenation of a
    containerfile instruction.
    """
    instruction = data['instruction']
    value = data['value']
    content = f'{instruction} {value}'

    return hashlib.sha256(content.encode()).hexdigest()
