SHELL := /bin/bash

.PHONY: prepare
prepare:
	@ mkdir -p _build

.PHONY: build
build:
	@ gcc hello.c -o _build/hello

.PHONY: install
install:
	@ install --mode=755 _build/hello /usr/local/bin

.PHONY: clean
clean:
	@ rm -rf _build/
