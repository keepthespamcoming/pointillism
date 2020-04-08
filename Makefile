IMAGE := tgrayson/pointillism
VERSION_NEW := $(shell ./bin/version_next)

FLASK_RUN_PORT?=5000
PYTHON := python3
VENV = .venv
VENV_BUILD = .venv.build
HOST ?= https://raw.githubusercontent.com

export HOST
export FLASK_RUN_PORT
export PYTHONPATH=.:$(VENV):$(VENV_BUILD)

server: compile
	@test -n "$(HOST)" # set $$HOST variable
	$(PYTHON) -m server

compile: $(VENV)
	$(PYTHON) -m pip install -t $(VENV) -r requirements.txt

compileAll: compile $(VENV_BUILD)
$(VENV_BUILD): requirements/build.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements/build.txt
	touch $(VENV_BUILD)
	
$(VENV): requirements.txt
	$(PYTHON) -m pip install -t $(VENV) -r requirements.txt
	touch $(VENV)

clean:
	find . -name "*.pyc" -delete
	rm -rf $(VENV) $(VENV_BUILD)
	# docker rm pointillism
	# docker rmi tgrayson/pointillism

image:
	docker build -t $(IMAGE) .

# confirmImage: image
# 	test docker run tgrayson/pointillism:latest

imagePush: 
	echo "$(DOCKER_PASS)" | docker login -u "$(DOCKER_USER)" --password-stdin
	docker push $(IMAGE)

deploy:
	# npm install serverless
	serverless deploy

versionBump:
	git pull --tags
	git tag $(VERSION_NEW)
	git push --tags
test: compileAll
	$(PYTHON) -m pytest

.PHONY: test
