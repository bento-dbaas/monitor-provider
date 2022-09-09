dev:
	export FLASK_DEBUG=1

run:
	export FLASK_APP=./monitor_provider/app.py; export FLASK_DEBUG=1; python -m flask run --host 0.0.0.0 --port=5004

run_dev:
	docker-compose up

deploy_dev:
	tsuru app-deploy -a monitor-provider-dev .

deploy_prod:
	tsuru app-deploy -a monitor-provider .

