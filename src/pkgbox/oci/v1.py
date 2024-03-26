from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Descriptor:
    alg: str
    digest: str

    def __str__(self) -> str:
        return f'{self.alg}:{self.digest}'

    @classmethod
    def from_str(cls, data: str) -> 'Layer':
        return cls(*data.split(':'))


@dataclass
class Manifest:
    schema_version: str = field(init=False)
    name: str
    tag: str
    architecture: str
    layers: List[Descriptor]
    history: List[str]
    signatures: Any
    digest: Descriptor

    def __post_init__(self) -> None:
        self.schema_version = 1
