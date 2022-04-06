import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.tcp_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.tcp_monitor.business import create_tcp_monitor, get_tcp_monitor, delete_tcp_monitor

ns = api.namespace('', description='Operations related to service_monitor')
provider_name = 'zabbix'


@ns.route('/zabbix/<string:env>/tcp/new')
class TcpMonitorCreate(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(tcp_monitor_serializer)
    @auth.login_required()
    def post(self, env):
        """
        Create new TCP Monitor for Zabbix
        """
        data = json.loads(request.data or 'null')
        return create_tcp_monitor(provider_name, env, data)


@ns.route('/zabbix/<string:env>/tcp/<string:identifier_or_name>')
class TcpMonitorItemGet(Resource):
    @auth.login_required()
    def get(self, env, identifier_or_name):
        """
        Return TCP Monitor based on env, identifier_or_name
        """
        return get_tcp_monitor(provider_name, env, identifier_or_name)


@ns.route('/zabbix/<string:env>/tcp/<string:identifier>')
class TcpMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, env, identifier):
        """
        Delete TCP Monitor based on env, identifier
        """
        return delete_tcp_monitor(provider_name, env, identifier)
