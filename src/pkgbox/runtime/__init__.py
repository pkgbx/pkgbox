from pkgbox import errors
from .meta import Runtime


def build(runtime_name: str) -> Runtime:
    """
    Create a new runtime object.
    """
    raise errors.PBNotImplementedError()
