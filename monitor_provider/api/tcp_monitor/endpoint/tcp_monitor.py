import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.tcp_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.tcp_monitor.business import create_tcp_monitor, get_tcp_monitor, delete_tcp_monitor

ns = api.namespace(path='/', name='TCP Monitor', description='Operations related to tcp_monitor')
provider_name = 'zabbix'


@ns.route('/zabbix/<string:env>/tcp/new')
@ns.doc(params={'env': 'This is the possible values to env'})
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
@ns.doc(params={'env': 'This is the possible values to env',
                'identifier_or_name': 'Identifier or name of Database'})
class TcpMonitorItemGet(Resource):
    @auth.login_required()
    def get(self, env, identifier_or_name):
        """
        Return TCP Monitor based on env, identifier_or_name
        """
        return get_tcp_monitor(provider_name, env, identifier_or_name)


@ns.route('/zabbix/<string:env>/tcp/<string:identifier>')
@ns.doc(params={'env': 'This is the possible values to env',
                'identifier': 'Identifier of Database'})
class TcpMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, env, identifier):
        """
        Delete TCP Monitor based on env, identifier
        """
        return delete_tcp_monitor(provider_name, env, identifier)
