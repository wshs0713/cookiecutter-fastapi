install:
	pip install pipenv && pipenv install --dev

test:
	pytest ./tests

linter-flake8:
	flake8 ./app

linter-pylint:
	pylint ./app

docstyle:
	pydocstyle ./app

build:.
	docker build -t {{cookiecutter.project_slug}}:$(VERSION) \
		--build-arg USER_ID=$(USER_ID) \
		--build-arg GID=$(GID) .

deploy:
	USER_ID=$(USER_ID) GID=$(GID) VERSION=$(VERSION) docker-compose up --build -d {{cookiecutter.project_slug}}
