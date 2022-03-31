import logging
import traceback
from flask_restplus import Api
from flask_httpauth import HTTPBasicAuth
from bson import json_util
from traceback import print_exc
from flask import jsonify, make_response
from monitor_provider import settings

log = logging.getLogger(__name__)

auth = HTTPBasicAuth()
api = Api(version='1.0', title='Monitor Provider API',
          description='API to manage monitor alarms', doc='/docs/')


@auth.verify_password
def verify_password(username, password):
    if settings.APP_USERNAME and username != settings.APP_USERNAME:
        return False
    if settings.APP_PASSWORD and password != settings.APP_PASSWORD:
        return False
    return True


def _response(status, **kwargs):
    content = jsonify(**kwargs)
    return make_response(content, status)


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


