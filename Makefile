run_local:
	docker-compose -f docker-compose-local.yml up --build

test:
	pytest

fmt:
	black --line-length 88 .
	isort .

fix:
	autoflake --in-place --remove-all-unused-imports --recursive .
	autopep8 --in-place --aggressive --aggressive --recursive --max-line-length 88 .

lint:
	flake8 .

check: fmt lint
fix_check: fmt fix lint