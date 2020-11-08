all:
	make .venv/bin/python
	make install-packages
	make setup-timelog

# output coloring & timing
include .scripts/init.mk

# virtual env creation, package updates, db migration
include .scripts/install.mk

setup:
	.venv/bin/python setup.py install

clean:
	rm -rf .venv