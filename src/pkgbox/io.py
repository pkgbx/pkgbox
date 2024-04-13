"""
IO library.
"""
import typing

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
        with open(self.path, 'r') as f:
            return f.read()


class HttpReader(Reader):
    def read(self) -> str:
        """
        Return the content of a given http(s) url using a
        GET request.
        """
        res = requests.get(f'{self.scheme}://{self.path}')

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
