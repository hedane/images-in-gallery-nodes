
.PHONY: lint
lint:
	docker run --rm -v "$(PWD)":/apps alpine/flake8 \
		--ignore=F401,E501 ./*.py

.PHONY: format
format:
	docker run --rm -v "$(PWD)":/code mercutiodesign/docker-black black \
		./*.py
