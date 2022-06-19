SSHELL = /bin/bash
package = shagen/puhdistusalue

.DEFAULT_GOAL := all
isort = isort puhdistusalue tests
black = black -S -l 120 --target-version py39 puhdistusalue tests

.PHONY: install
install:
	pip install -U pip wheel
	pip install -r tests/requirements.txt
	pip install -U .

.PHONY: install-all
install-all: install
	pip install -r tests/requirements-dev.txt

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: init
init:
	pip install -r tests/requirements.txt
	pip install -r tests/requirements-dev.txt

.PHONY: lint
lint:
	python setup.py check -ms
	flake8 puhdistusalue/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: mypy
mypy:
	mypy puhdistusalue

.PHONY: test
test: clean
	pytest --asyncio-mode=strict --cov=puhdistusalue --cov-report term-missing:skip-covered --cov-branch --log-format="%(levelname)s %(message)s"

.PHONY: testcov
testcov: test
	@echo "building coverage html"
	@coverage html

.PHONY: all
all: lint mypy testcov

.PHONY: clean
clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -rf .cache
	@rm -rf htmlcov
	@rm -rf *.egg-info
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -rf build
	@rm -f *.log
	python setup.py clean
	@git status

image:
	@echo "- building container image"
	set -e ;\
	RND_SEED=$$(openssl rand -base64 48) ;\
	BUILD_TS=$$(date -u +'%Y-%m-%dT%H:%M:%SZ') ;\
	REVISION=$$(git rev-parse --verify HEAD) ;\
	VERSION=$$(grep version setup.py | cut -f2 -d'"') ;\
	echo $$RND_SEED $$BUILD_TS ;\
	docker buildx use rekcod ;\
	docker buildx inspect rekcod ;\
	docker buildx build \
  	--output=type=registry \
	--platform linux/amd64,linux/arm64,linux/arm/v7 \
	--no-cache \
	--build-arg BUILD_TS=$$BUILD_TS \
	--build-arg REVISION=$$REVISION \
	--build-arg VERSION=$$VERSION \
	--tag $(package) . ;\

	@echo "Result: $$(docker inspect -f \
	'version={{index .Config.Labels "org.opencontainers.image.version"}}\
	timestamp={{index .Config.Labels "org.opencontainers.image.created"}}\
	revision=sha1:{{index .Config.Labels "org.opencontainers.image.revision"}}' \
	$(package))" ;\

available:
	@echo "- publishing container image on hub.docker.com"
	@echo " + docker inspect says:"
	@echo "   $$(docker inspect -f \
	'version={{index .Config.Labels "org.opencontainers.image.version"}}\
	timestamp={{index .Config.Labels "org.opencontainers.image.created"}}\
	revision=sha1:{{index .Config.Labels "org.opencontainers.image.revision"}}' \
	$(package))" ;\
	docker push $(package) ;\
