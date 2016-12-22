SHELL=/bin/bash
TEST_PATH=./tests

.PHONY: auto install test clean

auto: build35 install

build27:
	virtualenv local --python=python2.7 --never-download --system-site-packages

build32:
	virtualenv local --python=python3.2 --never-download --system-site-packages

build33:
	virtualenv local --python=python3.3 --never-download --system-site-packages

build34:
	virtualenv local --python=python3.4 --never-download --system-site-packages

build35:
	virtualenv local --python=python3.5 --never-download --system-site-packages

install:
	local/bin/pip install -r requirements.txt

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

test: clean-pyc
	. local/bin/activate && python -m pytest "$(TEST_PATH)"

clean: clean-pyc clean-build
	rm --recursive --force local
