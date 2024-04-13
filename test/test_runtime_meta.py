from pkgbox.runtime import meta


def test_instruction_ok():
    inst = meta.Instruction('RUN', 'make install')

    assert inst.digest == 'sha256:05d47cc1060b89d21df372e5a09ef5ed91e6e9dc2d8c7102abe464865155cfdd'
