import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.mongodb_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.mongodb_monitor.business import create_mongodb_monitor, get_mongodb_monitor, \
    delete_mongodb_monitor

ns = api.namespace(path='/', name='MongoDB Monitor', description='Operations related to mongodb_monitor')
provider_name = 'zabbix'


@ns.route('/zabbix/<string:env>/mongodb/new')
@ns.doc(params={'env': 'This is the possible values to env'})
class MongoDbMonitorCreate(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(mongodb_monitor_serializer)
    @auth.login_required()
    def post(self, env):
        """
        Create new MongoDB Monitor for Zabbix
        """
        data = json.loads(request.data or 'null')
        return create_mongodb_monitor(provider_name, env, data)


@ns.route('/zabbix/<string:env>/mongodb/<string:identifier_or_name>')
@ns.doc(params={'env': 'This is the possible values to env',
                'identifier_or_name': 'Identifier or name of Database'})
class MongoDbItemGet(Resource):
    @auth.login_required()
    def get(self, env, identifier_or_name):
        """
        Return MongoDB Monitor based on env, identifier_or_name
        """
        return get_mongodb_monitor(provider_name, env, identifier_or_name)


@ns.route('/zabbix/<string:env>/mongodb/<string:identifier>')
@ns.doc(params={'env': 'This is the possible values to env',
                'identifier': 'Identifier of Database'})
class MongoDbMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, env, identifier):
        """
        Delete MongoDB Monitor based on env, identifier
        """
        return delete_mongodb_monitor(provider_name, env, identifier)
