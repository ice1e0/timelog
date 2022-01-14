# virtual env creation, package updates, db migration

# determine the right python binary
.PYTHON3:=$(shell PATH='$(subst $(CURDIR)/.venv/bin:,,$(PATH))' which python3)

# create or update virtualenv
.venv/bin/python: 
# if .venv is already a symlink, don't overwrite it
	mkdir -p .venv

# go into the new dir and build it there as venv doesn't work if the target is a symlink
	cd .venv && $(.PYTHON3) -m venv --copies --prompt='[$(shell basename `pwd`)/.venv]' .

# install minimum set of required packages
# wheel needs to be early to be able to build wheels
	.venv/bin/pip install --upgrade wheel requests setuptools pipdeptree

# Workaround problems with un-vendored urllib3/requests in pip on ubuntu/debian
# This forces .venv/bin/pip to use the vendored versions of urllib3 from the installed requests version
# see https://stackoverflow.com/a/46970344/1380673
	-rm -vf .venv/share/python-wheels/{requests,chardet,urllib3}-*.whl

# install exact package versions from requirements.txt.freeze
install-packages:
	make -j .venv/bin/python
	.venv/bin/python -m pip install --upgrade pip wheel requests setuptools pipdeptree
	.venv/bin/python -m pip install --requirement=requirements.txt.freeze --src=./packages --upgrade --exists-action=w

# update packages from requirements.txt and create requirements.txt.freeze
update-packages:
	make -j .venv/bin/python
	.venv/bin/python -m pip install --upgrade pip wheel requests setuptools pipdeptree
	PYTHONWARNINGS="ignore" .venv/bin/python -m pip install --requirement=requirements.txt --src=./packages --upgrade --exists-action=w

# write freeze file
# pkg-ressources is automatically added on ubuntu, but breaks the install.
# https://stackoverflow.com/a/40167445/1380673
	.venv/bin/python -m pip freeze | grep -v "pkg-resources" > requirements.txt.freeze

	echo -e "\033[32msucceeded, please check output above for warnings\033[0m"
