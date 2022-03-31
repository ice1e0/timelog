all:
	make .venv/bin/python
	make install-packages
	make setup

# output coloring & timing
include .scripts/init.mk

# virtual env creation, package updates, db migration
include .scripts/install.mk

build:
	.venv/bin/python -m build

clean:
	rm -rf .venv