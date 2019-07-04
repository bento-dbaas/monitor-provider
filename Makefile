dev:
	export FLASK_DEBUG=1

run:
	export FLASK_APP=./monitor_provider/app.py; python -m flask run

deploy_dev:
	tsuru app-deploy -a monitor-provider-dev .

deploy_prod:
	tsuru app-deploy -a monitor-provider-api .

