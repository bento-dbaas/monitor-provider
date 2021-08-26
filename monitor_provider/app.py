import logging
import json
from bson import json_util
from traceback import print_exc
from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from mongoengine import connect
from monitor_provider.providers import get_provider_to
from monitor_provider.settings import (
    APP_USERNAME,
    APP_PASSWORD,
    LOGGING_LEVEL,
    MONGODB_DB,
    MONGODB_PARAMS)

app = Flask(__name__)
auth = HTTPBasicAuth()
connect(MONGODB_DB, **MONGODB_PARAMS)
logging.basicConfig(
    level=LOGGING_LEVEL,
    format='%(asctime)s %(filename)s(%(lineno)d) %(levelname)s: %(message)s')


@auth.verify_password
def verify_password(username, password):
    if APP_USERNAME and username != APP_USERNAME:
        return False

    if APP_PASSWORD and password != APP_PASSWORD:
        return False

    return True


@app.route(
    "/<string:provider_name>/<string:env>/credential/new",
    methods=['POST'])
@auth.login_required
def create_credential(provider_name, env):
    data = json.loads(request.data or 'null')
    if not data:
        logging.error("No data")
        return response_invalid_request("No data".format(data))
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        success, message = provider.credential_add(data)
    except Exception as e:
        print_exc()  # TODO Improve log
        return response_invalid_request(str(e))

    if not success:
        return response_invalid_request(message)
    return response_created(success=success, id=str(message))


@app.route(
    "/<string:provider_name>/credentials",
    methods=['GET'])
@auth.login_required
def get_all_credential(provider_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(None)
        return make_response(
            json.dumps(
                list(map(lambda x: x, provider.credential.all())),
                default=json_util.default
            )
        )
    except Exception as e:
        print_exc()  # TODO Improve log
        return response_invalid_request(str(e))


@app.route(
    "/<string:provider_name>/<string:env>/credential",
    methods=['GET'])
@auth.login_required
def get_credential(provider_name, env):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        credential = provider.credential.get_by(environment=env)
    except Exception as e:
        print_exc()  # TODO Improve log
        return response_invalid_request(str(e))

    if credential.count() == 0:
        return response_not_found('{}/{}'.format(provider_name, env))
    return make_response(json.dumps(credential[0], default=json_util.default))


@app.route("/<string:provider_name>/<string:env>/credential", methods=['PUT'])
@auth.login_required
def update_credential(provider_name, env):
    return create_credential(provider_name, env)


@app.route(
    "/<string:provider_name>/<string:env>/credential",
    methods=['DELETE'])
@auth.login_required
def destroy_credential(provider_name, env):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        deleted = provider.credential.delete()
    except Exception as e:
        print_exc()  # TODO Improve log
        return response_invalid_request(str(e))

    if deleted['n'] > 0:
        return response_ok()
    return response_not_found("{}-{}".format(provider_name, env))


def response_invalid_request(error, status_code=500):
    return _response(status_code, error=error)


def response_not_found(identifier):
    error = "Could not found with {}".format(identifier)
    return _response(404, error=error)


def response_created(status_code=201, **kwargs):
    return _response(status_code, **kwargs)


def response_ok(**kwargs):
    if kwargs:
        return _response(200, **kwargs)
    return _response(200, message="ok")


def _response(status, **kwargs):
    content = jsonify(**kwargs)
    return make_response(content, status)


@app.route("/<string:provider_name>/<string:env>/service/new",
    methods=['POST'])
@auth.login_required
def create_service_monitor(provider_name, env):
    data = json.loads(request.data or 'null')
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        service = provider.create_service_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=service.identifier)


@app.route(
    "/<string:provider_name>/<string:env>/service/<string:identifier_or_name>",
    methods=['GET'])
@auth.login_required
def get_service_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    service = provider.get_service_monitor(identifier_or_name)
    if not service:
        return response_not_found(identifier_or_name)
    return response_ok(**service.get_json)


@app.route(
    "/<string:provider_name>/<string:env>/service/<string:identifier>",
    methods=['DELETE'])
@auth.login_required
def delete_service_monitor(provider_name, env, identifier):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_service_monitor(identifier)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()


@app.route(
    "/<string:provider_name>/<string:env>/host/new",
    methods=['POST'])
@auth.login_required
def create_host_monitor(provider_name, env):
    data = json.loads(request.data or 'null')
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        host = provider.create_host_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=host.identifier)


@app.route(
    "/<string:provider_name>/<string:env>/host/<string:identifier_or_name>",
    methods=['GET'])
@auth.login_required
def get_host_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    host = provider.get_host_monitor(identifier_or_name)
    if not host:
        return response_not_found(identifier_or_name)
    return response_ok(**host.get_json)


@app.route(
    "/<string:provider_name>/<string:env>/host/<string:identifier>",
    methods=['DELETE'])
@auth.login_required
def delete_host_monitor(provider_name, env, identifier):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_host_monitor(identifier)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()


@app.route(
    "/<string:provider_name>/<string:env>/web/new",
    methods=['POST'])
@auth.login_required
def create_web_monitor(provider_name, env):
    data = json.loads(request.data or 'null')
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        web = provider.create_web_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=web.identifier)


@app.route(
    "/<string:provider_name>/<string:env>/web/<string:identifier_or_name>",
    methods=['GET'])
@auth.login_required
def get_web_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    host = provider.get_web_monitor(identifier_or_name)
    if not host:
        return response_not_found(identifier_or_name)
    return response_ok(**host.get_json)


@app.route(
    "/<string:provider_name>/<string:env>/web/<string:identifier>",
    methods=['DELETE'])
@auth.login_required
def delete_web_monitor(provider_name, env, identifier):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_web_monitor(identifier)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()


@app.route(
    "/<string:provider_name>/<string:env>/database_cassandra/new",
    methods=['POST'])
@auth.login_required
def create_database_cassandra_monitor(provider_name, env):
    data = json.loads(request.data or 'null')
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        monitor = provider.create_database_cassandra_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    return response_created(success=True, identifier=monitor.identifier)


@app.route(
    "/<string:provider_name>/<string:env>/database_cassandra/<string:identifier_or_name>",
    methods=['GET'])
@auth.login_required
def get_database_cassandra_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    database = provider.get_database_cassandra_monitor(identifier_or_name)
    if not database:
        return response_not_found(identifier_or_name)
    return response_ok(**database.get_json)


@app.route(
    "/<string:provider_name>/<string:env>/database_cassandra/<string:database_name>",
    methods=['DELETE'])
@auth.login_required
def delete_database_cassandra_monitor(provider_name, env, database_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_database_cassandra_monitor(database_name)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()

@app.route(
    "/<string:provider_name>/<string:env>/instance_cassandra/new",
    methods=['POST'])
@auth.login_required
def create_instance_cassandra_monitor(provider_name, env):
    data = json.loads(request.data or 'null')
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        monitor = provider.create_instance_cassandra_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=monitor.identifier)


@app.route(
    "/<string:provider_name>/<string:env>/instance_cassandra/<string:identifier_or_name>",
    methods=['GET'])
@auth.login_required
def get_instance_cassandra_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    database = provider.get_instance_cassandra_monitor(identifier_or_name)
    if not database:
        return response_not_found(identifier_or_name)
    return response_ok(**database.get_json)


@app.route(
    "/<string:provider_name>/<string:env>/instance_cassandra/<string:instance_name>",
    methods=['DELETE'])
@auth.login_required
def delete_instance_cassandra_monitor(provider_name, env, instance_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_instance_cassandra_monitor(instance_name)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()
