import os
import logging
import werkzeug
import flask.scaffold
werkzeug.cached_property = werkzeug.utils.cached_property
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import Flask, Blueprint
from monitor_provider.api.restplus import api
from monitor_provider.api.credential.endpoint.credential import ns as credential_namespace
from monitor_provider.api.database_monitor.endpoint.database_monitor import ns as database_monitor_namespace
from monitor_provider.api.host_monitor.endpoint.host_monitor import ns as host_monitor_namespace
from monitor_provider.api.instance_monitor.endpoint.instance_monitor import ns as instance_monitor_namespace
from monitor_provider.api.mysql_monitor.endpoint.mysql_monitor import ns as mysql_monitor_namespace
from monitor_provider.api.service_monitor.endpoint.service_monitor import ns as service_monitor_namespace
from monitor_provider.api.tcp_monitor.endpoint.tcp_monitor import ns as tcp_monitor_namespace
from monitor_provider.api.web_monitor.endpoint.web_monitor import ns as web_monitor_namespace
from monitor_provider.api.mongodb_monitor.endpoint.mongodb_monitor import ns as mongodb_monitor_namespace
from flask_mongoengine import MongoEngine
from monitor_provider import settings

db = MongoEngine()
app = Flask(__name__)
log = logging.getLogger(__name__)
logging.basicConfig(
    level=settings.LOGGING_LEVEL,
    format='%(asctime)s %(filename)s(%(lineno)d) %(levelname)s: %(message)s')


def configure_app(flask_app):
    print(settings.MONGODB_PARAMS)
    flask_app.config['MONGODB_SETTINGS'] = settings.MONGODB_PARAMS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/')
    api.init_app(blueprint)
    api.add_namespace(credential_namespace)
    api.add_namespace(database_monitor_namespace)
    api.add_namespace(host_monitor_namespace)
    api.add_namespace(instance_monitor_namespace)
    api.add_namespace(mysql_monitor_namespace)
    api.add_namespace(service_monitor_namespace)
    api.add_namespace(tcp_monitor_namespace)
    api.add_namespace(web_monitor_namespace)
    api.add_namespace(mongodb_monitor_namespace)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format('localhost:5000'))
    app.run(debug=True)


initialize_app(app)


if __name__ == '__main__':
    main()
