"""
Runtime "meta module" that defines interfaces
to be used by implementations.
"""
import hashlib
from typing import Protocol
from dataclasses import dataclass, field


@dataclass
class Instruction:
    """
    Dataclass that represents a build instruction
    to be executed by a runtime implementation.

    "ctx" represents the type or context of instruction while
    "cmd" the instruction command itself.

    Assuming the following Containerfile line "RUN make install",
    "ctx" = "RUN" and "cmd" = "make install".

    This class has an "digest" proiperty which is automatically filled,
    with a hash digest (sha256) of both inst_type and inst_cmd.
    """
    ctx: str
    cmd: str
    inst_digest: str = field(init=False)
    
    def __post_init__(self) -> None:
        """
        Sets the value of `self.inst_digest` after the object initialization.
        """
        typecmd = f'{self.ctx}{self.cmd}'
        hashed = hashlib.sha256(typecmd.encode()).hexdigest()

        self.digest = f'sha256:{hashed}'

    def __eq__(self, other: 'Instruction') -> bool:
        """
        Check two Intruction objects are the same by comparing its
        digest value.
        """
        return self.digest == other.digest

    def __eq__(self, other: 'Instruction') -> bool:
        """
        Check two Intruction objects are not the same by comparing its
        digest value.
        """
        return self.digest != other.digest


class Runtime(Protocol):
    """
    Runtime protocol to be implemented
    by other classes.

    A "Runtime" implementation will implement
    the steps and phases of a build runtime.
    """
    def prepare_build(self, build_id: str) -> None:
        """
        Prepares a build to be run, create files, pull
        base images, etc.
        """
        pass
    
    def run_build_instruction(self, build_id: str, instruction: Instruction) -> None:
        """
        Run a build instruction.

        Implementations should raise `pkgbox.errors.PBRuntimeError`
        in case of errors.
        """
        pass
