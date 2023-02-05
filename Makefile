.PHONY: all clean lint flake8 autopep8 pylint

all: lint

clean:
	rm -rf build dist *egg-info ./__pycache__
	find -name *.pyc -delete

###############
# Development #
###############

.PHONY: pip-freeze requirements.txt dev-requirements.txt

##########
# Verify #
##########

lint: flake8 pylint black

black:
	black --check --diff src/

format:
	black src/

flake8:
	flake8 .

autopep8:
	autopep8 --recursive --in-place .

pylint:
	pylint src/
