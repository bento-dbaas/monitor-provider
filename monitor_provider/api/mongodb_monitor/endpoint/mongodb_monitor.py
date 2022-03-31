import logging
import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.mongodb_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.mysql_monitor.business import create_mysql_monitor, get_mysql_monitor, delete_mysql_monitor

ns = api.namespace('', description='Operations related to service_monitor')
provider_name = 'zabbix'


@ns.route('/zabbix/<string:env>/mongodb/new')
class MongoDbMonitorCreate(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(mongodb_monitor_serializer)
    @auth.login_required()
    def post(self, env):
        data = json.loads(request.data or 'null')
        return create_mysql_monitor(provider_name, env, data)


@ns.route('/zabbix/<string:env>/mongodb/<string:identifier_or_name>')
class MongoDbItemGet(Resource):
    @auth.login_required()
    def get(self, env, identifier_or_name):
        """
        Return Service Monitor based on provider name and env
        """
        return get_mysql_monitor(provider_name, env, identifier_or_name)


@ns.route('/zabbix/<string:env>/mongodb/<string:identifier>')
class MongoDbMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, env, identifier):
        """
        Delete Service Monitor based on provider name and env
        """
        return delete_mysql_monitor(provider_name, env, identifier)
