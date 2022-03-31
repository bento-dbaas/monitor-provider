import logging
import json
from bson import json_util
from monitor_provider.api.restplus import response_invalid_request, response_created, response_not_found, response_ok, \
    _response
from flask import make_response
from monitor_provider.providers import get_provider_to
from traceback import print_exc


def get_all_credentials(provider_name):
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


def create_credential(provider_name, env, data):
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


def delete_credential(provider_name, env):
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



