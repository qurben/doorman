default: test

test:
	nosetests tests

coverage:
	nosetests --with-coverage --cover-erase --cover-html --cover-package=doorman tests

dep:
	pip install -r requirements.txt --use-mirrors

install:
	python setup.py install
