import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.host_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.host_monitor.business import create_host_monitor, get_host_monitor, delete_host_monitor


ns = api.namespace(path='/', name='Host Monitor', description='Operations related to host_monitor')


@ns.route('/dbmonitor/<string:env>/host/new')
@ns.doc(params={'env': 'This is the possible values to env'})
class HostMonitorDbMonitorCollection(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(host_monitor_dbmonitor_serializer)
    @auth.login_required()
    def post(self, env):
        """
        Create new Host Monitor for DbMonitor
        """
        provider_name = 'dbmonitor'
        data = json.loads(request.data or 'null')
        return create_host_monitor(provider_name, env, data)


@ns.route('/zabbix/<string:env>/host/new')
@ns.doc(params={'env': 'This is the possible values to env'})
class HostMonitorDbMonitorCollection(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(host_monitor_zabbix_serializer)
    @auth.login_required()
    def post(self, env):
        """
        Create new Host Monitor for Zabbix
        """
        provider_name = 'zabbix'
        data = json.loads(request.data or 'null')
        return create_host_monitor(provider_name, env, data)


@ns.route('/<string:provider_name>/<string:env>/host/<string:identifier_or_name>')
@ns.doc(params={'provider_name': 'This is the possible values to provider_name',
                'env': 'This is the possible values to env',
                'identifier_or_name': 'Identifier or name of Database'})
class HostMonitorItemGet(Resource):
    @auth.login_required()
    def get(self, provider_name, env, identifier_or_name):
        """
        Return Host Monitor based on provider name, env, identifier
        """
        return get_host_monitor(provider_name, env, identifier_or_name)


@ns.route('/<string:provider_name>/<string:env>/host/<string:identifier>')
@ns.doc(params={'provider_name': 'This is the possible values to provider_name',
                'env': 'This is the possible values to env',
                'identifier': 'Identifier of Database'})
class HostMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, provider_name, env, identifier):
        """
        Delete Host Monitor based on provider_name, env, identifier
        """
        return delete_host_monitor(provider_name, env, identifier)

