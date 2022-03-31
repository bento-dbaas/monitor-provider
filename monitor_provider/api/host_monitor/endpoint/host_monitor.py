import logging
import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.host_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.host_monitor.business import create_host_monitor, get_host_monitor, delete_host_monitor


ns = api.namespace('', description='Operations related to host_monitor')


@ns.route('/dbmonitor/<string:env>/host/new')
class HostMonitorDbMonitorCollection(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(host_monitor_dbmonitor_serializer)
    @auth.login_required()
    def post(self, provider_name, env):
        data = json.loads(request.data or 'null')
        return create_host_monitor(provider_name, env, data)


@ns.route('/zabbix/<string:env>/host/new')
class HostMonitorDbMonitorCollection(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(host_monitor_zabbix_serializer)
    @auth.login_required()
    def post(self, provider_name, env):
        data = json.loads(request.data or 'null')
        return create_host_monitor(provider_name, env, data)


@ns.route('/<string:provider_name>/<string:env>/host/<string:identifier_or_name>')
class ServiceMonitorItem(Resource):
    @auth.login_required()
    def get(self, provider_name, env, identifier_or_name):
        """
        Return Service Monitor based on provider name and env
        """
        return get_host_monitor(provider_name, env, identifier_or_name)

    @auth.login_required()
    def delete(self, provider_name, env, identifier_or_name):
        """
        Delete Service Monitor based on provider name and env
        """
        return delete_host_monitor(provider_name, env, identifier_or_name)
