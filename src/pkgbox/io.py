"""
IO library.
"""
import typing

from . import errors

import requests


class Reader(typing.Protocol):
    """
    Reader Protocol to be implemented by other classes.
    """
    def __init__(self, scheme: str, path: str) -> None:
        self.scheme = scheme
        self.path = path
    
    def read(self) -> str: pass


class FileReader(Reader):
    def read(self) -> str:
        """
        Return the file content of a given path.
        """
        try:
            with open(self.path, 'r') as f:
                return f.read()
        except OSError as e:
            raise errors.PBError(str(e), e.errno)


class HttpReader(Reader):
    def read(self) -> str:
        """
        Return the content of a given http(s) url using a
        GET request.
        """
        try:
            res = requests.get(f'{self.scheme}://{self.path}')
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise errors.PBError(str(e), e.response.status_code)

        return res.text


def build_reader(scheme: str, value: str) -> Reader:
    """
    Build a reader specialized object based on
    the provided scheme.
    """
    ref = {
        'file': FileReader,
        'http': HttpReader,
        'https': HttpReader
    }

    return ref.get(scheme, FileReader)(scheme, value)
