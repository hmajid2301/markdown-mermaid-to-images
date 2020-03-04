# prompt_example> make test PY=py35 OPTIONS="-- -s"
.PHONY: test
test:
	@tox -e $(OPTIONS)

.PHONY: install-venv
install-venv:
	@tox -e dev

.PHONY: lint
lint:
	@tox -e lint

.PHONY: code-formatter
code-formatter:
	@tox -e code-formatter

.PHONY: code-formatter-check
code-formatter-check:
	@tox -e code-formatter -- --check

# prompt_example> make bumpversion OPTIONS="-- --allow-dirty patch"
.PHONY: bumpversion
bumpversion:
	@tox -e bumpversion $(OPTIONS)

.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@find . -type d -name '*.ropeproject' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -f src/*.egg
	@rm -f src/*.eggs
	@rm -rf src/*.egg-info/
	@rm -f MANIFEST
	@rm -rf docs/build/
	@rm -rf htmlcov/
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -rf .cache/
	@rm -f coverage.xml
	@rm -f *.cover
	@rm -rf .pytest_cache/

.PHONY: install-dev
install-dev:
	@pip install -e .

.PHONY: build-dist
build-dist:
	@python setup.py sdist

.PHONY: check-manifest
check-manifest:
	@tox -e check-manifest

.PHONY: pypi-check
pypi-check:
	make build-dist
	@tox -e pypi-check

# prompt_example> make pypi OPTIONS="-- --repository-url https://test.pypi.org/legacy/"
.PHONY: pypi-upload
pypi-upload:
	@tox -e pypi-upload $(OPTIONS)