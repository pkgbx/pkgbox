SHELL := /bin/bash
PY_CMD := poetry run python
PYTEST_CMD := ${PY_CMD} -m pytest
TEST_DIR := test/

.PHONY: test
test:
	${PYTEST_CMD} ${TEST_DIR}
