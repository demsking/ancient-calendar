APP_NAME := $(shell python scripts/metadata.py name)
APP_VERSION := $(shell python scripts/metadata.py version)
IMAGE_NAME := demsking/$(APP_NAME)


# Start the development environment using tmuxinator
shell:
	tmuxinator

stop:
	tmux kill-session -t ancient-calendar

up: pull
	docker compose -f .devcontainer/workspace.yaml up -d --remove-orphans

.PHONY: config
config:
	docker compose -f .devcontainer/workspace.yaml config

logs:
	docker compose -f .devcontainer/workspace.yaml logs -f

pull:
	docker compose -f .devcontainer/workspace.yaml pull

restart:
	docker compose -f .devcontainer/workspace.yaml restart

down:
	docker compose -f .devcontainer/workspace.yaml down

stats:
	docker compose -f .devcontainer/workspace.yaml stats

gen-tests:
	python scripts/gen.py

test: gen-tests
	pytest -vv

coverage:
	pytest --cov=server

coverage-html:
	pytest --cov=server --cov-report=html

lint:
	pre-commit run --all-files

fix:
	ruff check . --fix

#
## Dependencies
install:
	poetry install

outdated:
	poetry show --outdated

update:
	poetry update
	devbox update
	pre-commit autoupdate


#
## Documentation
.PHONY: doc/openapi.json
doc/openapi.json: DOCUMENTATION.md
	python scripts/generate-openapi.py > $@

resources: doc/openapi.json

#
## Packaging
build/context:
	docker buildx create --name $(APP_NAME) --bootstrap
	mkdir -p build/
	touch $@

build/requirements.txt: pyproject.toml poetry.lock
	mkdir -p build/
	poetry export --only=main --without-hashes -f requirements.txt -o $@

image: build/context build/requirements.txt resources
	docker buildx use $(APP_NAME)
	docker buildx build . \
	  --platform linux/amd64,linux/arm64 \
	  --push \
	  --progress plain \
	  --tag $(IMAGE_NAME):$(APP_VERSION) \
	  --tag $(IMAGE_NAME):latest \
	  --label "org.opencontainers.image.title=$(APP_NAME)" \
	  --label "org.opencontainers.image.description=$(shell python scripts/metadata.py description)" \
	  --label "org.opencontainers.image.version=$(APP_VERSION)" \
	  --label "org.opencontainers.image.revision=$(shell git rev-parse HEAD)" \
	  --label "org.opencontainers.image.authors=$(shell python scripts/metadata.py authors)" \
	  --label "org.opencontainers.image.created=$(shell date --rfc-3339=seconds)" \
	  --label "org.opencontainers.image.source=$(shell python scripts/metadata.py repository)" \
	  --label "org.opencontainers.image.url=$(shell python scripts/metadata.py repository)" \
	  --label "org.opencontainers.image.documentation=$(shell python scripts/metadata.py documentation)" \
	  --label "org.opencontainers.image.vendor=Sébastien Demanou" \
	  --label "org.opencontainers.image.licenses=$(shell python scripts/metadata.py license)"

image-test: build/requirements.txt
	docker build --debug . \
	  --progress plain \
	  --tag $(IMAGE_NAME):test

publish: resources image-test
	# git commit pyproject.toml -m "Release $(APP_VERSION)"
	$(MAKE) image
	git tag v$(APP_VERSION)
	git push --tags origin main
