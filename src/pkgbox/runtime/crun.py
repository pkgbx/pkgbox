"""
Pkgbox runtime implementation that uses the crun cli
to run builds in linux containers.
"""
import os
import errno
import shutil
from typing import Any

from pkgbox import errors
from .meta import Instruction, Runtime


class CrunRuntime(Runtime):
    """
    Crun runtime implementation.
    """
    def preflight_check(self) -> None:
        """
        Check if "crun" is available in $PATH and
        perms (+x) are in place.

        Raise `pkgbox.errors.PBRuntimeError` in case of errors.
        """
        crun_path = shutil.which('crun')

        if crun_path is None:
            raise errors.PBRuntimeError('Cannot find "crun" in $PATH')
        
        if not os.access(crun_path, os.X_OK):
            raise errors.PBRuntimeError('Not enough perms to run "{crun_path}"')

    def prepare_build(self, spec: Any, **kwargs: Any) -> None:
        """
        Prepare a build to run:

        - Check and validate the build spec
        - Prepare build directories/files, including crun's config.json file
        """
        labels = spec['labels']
        version = labels['org.pkgbox.schema.version']
        pkg_name = labels['org.pkgbox.package.name']
        pkg_version = labels['org.pkgbox.package.version']
        pkg_release = labels['org.pkgbox.package.release']

        if version != 1:
            raise errors.PBRuntimeError('Unsupported value for "org.pkgbox.schema.version"')
    
    def run_build(self, spec: Any) -> None:
        """
        Run all build insructions based on the passed spec.

        This function yields for each built instruction and the caller
        needs to deal with it as an iterator.

        Raise `pkgbox.errors.PBRuntimeError" in case of unexpected problems.
        """
        pass
