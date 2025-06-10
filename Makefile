run_local:
	docker-compose -f docker-compose-local.yml up --build

make test:
	pytest