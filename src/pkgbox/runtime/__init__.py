from pkgbox import errors
from .meta import Runtime
from .crun import CrunRuntime


_REF = {
    'crun': CrunRuntime
}


def build(runtime_name: str) -> Runtime:
    """
    Create a new runtime object.
    """
    impl = _REF.get(runtime_name)

    if impl is None:
        raise errors.PBRuntimeError(f'Invalid runtime: {runtime_name}')

    return impl()
