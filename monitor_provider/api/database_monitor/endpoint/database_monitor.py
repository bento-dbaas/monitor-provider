import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.database_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.database_monitor.business import create_database_monitor, get_database_monitor, \
    delete_database_monitor

ns = api.namespace('', description='Operations related to database_monitor')


@ns.route('/<string:provider_name>/<string:env>/database/cassandra/new')
class DatabaseMonitorCassandraCollection(Resource):
    @api.response(201, "Database Monitor successfully created")
    @api.expect(database_monitor_cassandra_serializer)
    @auth.login_required()
    def post(self, provider_name, env):
        """
        Create new Database Monitor for Cassandra Database
        """
        dbms = 'cassandra'
        data = json.loads(request.data or 'null')
        return create_database_monitor(provider_name, env, dbms, data)


@ns.route('/<string:provider_name>/<string:env>/database/postgresql/new')
class DatabaseMonitorPostgreSqlCollection(Resource):
    @api.response(201, "Database Monitor successfully created")
    @api.expect(database_monitor_postgresql_serializer)
    @auth.login_required()
    def post(self, provider_name, env):
        """
        Create new Database Monitor for PostgreSQL Database
        """
        dbms = 'postgresql'
        data = json.loads(request.data or 'null')
        return create_database_monitor(provider_name, env, dbms, data)


@ns.route('/<string:provider_name>/<string:env>/database/mongodb/new')
class DatabaseMonitorMongoDbCollection(Resource):
    @api.response(201, "Database Monitor successfully created")
    @api.expect(database_monitor_mongodb_serializer)
    @auth.login_required()
    def post(self, provider_name, env):
        """
        Create new Database Monitor for MongoDB Database
        """
        dbms = 'mongodb'
        data = json.loads(request.data or 'null')
        return create_database_monitor(provider_name, env, dbms, data)


@ns.route('/<string:provider_name>/<string:env>/database/<string:identifier_or_name>')
class DatabaseMonitorItemGet(Resource):
    @auth.login_required()
    def get(self, provider_name, env, identifier_or_name):
        """
        Return Database Monitor based on provider name, env, identifier
        """
        return get_database_monitor(provider_name, env, identifier_or_name)


@ns.route('/<string:provider_name>/<string:env>/database/<string:database_name>')
class DatabaseMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, provider_name, env, database_name):
        """
        Delete Database Monitor based on provider name, env, database_name
        """
        return delete_database_monitor(provider_name, env, database_name)
