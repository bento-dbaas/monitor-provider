import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.mysql_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.mysql_monitor.business import create_mysql_monitor, get_mysql_monitor, delete_mysql_monitor

ns = api.namespace('', description='Operations related to service_monitor')
provider_name = 'zabbix'


@ns.route('/zabbix/<string:env>/mysql/new')
class MysqlMonitorCreate(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(mysql_monitor_serializer)
    @auth.login_required()
    def post(self, env):
        """
        Create new MySQL Monitor for Zabbix
        """
        data = json.loads(request.data or 'null')
        return create_mysql_monitor(provider_name, env, data)


@ns.route('/zabbix/<string:env>/mysql/<string:identifier_or_name>')
class MysqlMonitorItemGet(Resource):
    @auth.login_required()
    def get(self, env, identifier_or_name):
        """
        Return MySQL Monitor based on provider env, identifier_or_name
        """
        return get_mysql_monitor(provider_name, env, identifier_or_name)


@ns.route('/zabbix/<string:env>/mysql/<string:identifier>')
class MysqlMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, env, identifier):
        """
        Delete MySQL Monitor based on env, identifier
        """
        return delete_mysql_monitor(provider_name, env, identifier)
