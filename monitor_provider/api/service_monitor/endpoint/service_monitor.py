import logging
import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.service_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.service_monitor.business import create_service_monitor, get_service_monitor, \
    delete_service_monitor

ns = api.namespace('', description='Operations related to service_monitor')
provider_name = 'dbmonitor'


@ns.route('/dbmonitor/<string:env>/service/new')
class ServiceMonitorCollection(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(service_monitor_serializer)
    @auth.login_required()
    def post(self, env):
        data = json.loads(request.data or 'null')
        return create_service_monitor(provider_name, env, data)


@ns.route('/dbmonitor/<string:env>/service/<string:identifier_or_name>')
class ServiceMonitorItem(Resource):
    @auth.login_required()
    def get(self, env, identifier_or_name):
        """
        Return Service Monitor based on provider name and env
        """
        return get_service_monitor(provider_name, env, identifier_or_name)

    @auth.login_required()
    def delete(self, env, identifier_or_name):
        """
        Delete Service Monitor based on provider name and env
        """
        return delete_service_monitor(provider_name, env, identifier_or_name)
