
.PHONY: lint
lint:
	docker run --rm -v "$(PWD)":/apps registry.idaddy.cn/mirror/flake8 \
		--ignore=F401,E501 ./*.py

.PHONY: format
format:
	docker run --rm -v "$(PWD)":/code registry.idaddy.cn/mirror/black black \
		./*.py
