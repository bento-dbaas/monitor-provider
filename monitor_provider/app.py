import logging
import json
from bson import json_util
from traceback import print_exc
from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from monitor_provider.providers import get_provider_to
from monitor_provider.settings import APP_USERNAME, APP_PASSWORD

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if APP_USERNAME and username != APP_USERNAME:
        return False

    if APP_PASSWORD and password != APP_PASSWORD:
        return False

    return True


@app.route(
    "/<string:provider_name>/<string:env>/credential/new", methods=['POST']
)
@auth.login_required
def create_credential(provider_name, env):
    data = json.loads(request.data or 'null')
    if not data:
        print("no data")
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
    "/<string:provider_name>/credentials", methods=['GET']
)
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
    "/<string:provider_name>/<string:env>/credential", methods=['GET']
)
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
    "/<string:provider_name>/<string:env>/credential", methods=['DELETE']
)
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


@app.route("/<string:provider_name>/<string:env>/host/new", methods=['POST'])
@auth.login_required
def register_host(provider_name, env):
    data = json.loads(request.data or 'null')
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        host_id = provider.register_host(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    return response_created(success=True, id=host_id)

@app.route(
    "/<string:provider_name>/<string:env>/host/<string:host_name>",
    methods=['GET']
)
@auth.login_required
def get_host(provider_name, env, host_name):
    if not host_name:
        return response_invalid_request("invalid data")
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        host = provider.get_host(host_name)
        return make_response(host.to_json)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))


@app.route(
    "/<string:provider_name>/<string:env>/host/<int:host_id>",
    methods=['DELETE']
)
@auth.login_required
def delete_host(provider_name, env, host_id):
    if not host_id:
        return response_invalid_request("invalid data")
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_host(host_id)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    return response_ok()


@app.route(
    "/<string:provider_name>/<string:env>/service/<string:service_name>",
    methods=['GET']
)
@auth.login_required
def get_service(provider_name, env, service_name):
    if not service_name:
        return response_invalid_request("invalid data")
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        service = provider.get_service(service_name)
        return make_response(service.to_json)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

@app.route("/<string:provider_name>/<string:env>/service/new", methods=['POST'])
@auth.login_required
def register_service(provider_name, env):
    data = json.loads(request.data or 'null')
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        service_id = provider.register_service(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    return response_created(success=True, id=service_id)