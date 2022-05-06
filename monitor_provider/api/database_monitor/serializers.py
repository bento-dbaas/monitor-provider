from flask_restplus import fields
from monitor_provider.api.restplus import api

database_monitor_cassandra_serializer = api.model('DatabaseMonitorCassandra', {
    'database_name': fields.String(required=True, description='Database Name', max_length=200, example='string'),
    'port': fields.String(required=True, description='Port', max_length=200, example='string'),
    'version': fields.String(required=True, description='Version', max_length=200, example='string'),
    'username': fields.String(required=True, description='Username', max_length=200, example='string'),
    'password': fields.String(required=True, description='Password', max_length=200, example='string'),
    'environment': fields.String(required=False, description='Environment', max_length=200, example='string'),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200, example='string'),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200, example='string'),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200, example='string'),
})

database_monitor_postgresql_serializer = api.model('DatabaseMonitorPostgreSQL', {
    'database_name': fields.String(required=True, description='Service Name', max_length=200, example='string'),
    'port': fields.String(required=True, description='Port', max_length=200, example='string'),
    'version': fields.String(required=True, description='Version', max_length=200, example='string'),
    'username': fields.String(required=True, description='Username', max_length=200, example='string'),
    'password': fields.String(required=True, description='Password', max_length=200, example='string'),
    'dns': fields.String(required=True, description='DNS', max_length=200, example='string'),
    'topology': fields.String(required=True, description='Topology options are: POSTGRESQL_SINGLE, POSTGRESQL_STANDBY.',
                              max_length=200, example='string'),
    'environment': fields.String(required=False, description='Environment', max_length=200, example='string'),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200, example='string'),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200, example='string'),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200,
                                       example='string'),
})


database_monitor_mongodb_serializer = api.model('DatabaseMonitorMongoDB', {
    'database_name': fields.String(required=True, description='Service Name', max_length=15, example='string'),
    'port': fields.String(required=True, description='Port', max_length=200, example='string'),
    'version': fields.String(required=True, description='Version', max_length=200, example='string'),
    'username': fields.String(required=True, description='Username', max_length=200, example='string'),
    'password': fields.String(required=True, description='Password', max_length=200, example='string'),
    'dns': fields.String(required=True, description='DNS', max_length=200, example='string'),
    'topology': fields.String(required=True, description='Topology options are: MONGODB_SINGLE , MONGODB_REPLICA_SET .',
                              max_length=200, example='string'),
    'environment': fields.String(required=False, description='Environment', max_length=200, example='string'),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200, example='string'),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200, example='string'),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200,
                                       example='string'),
})
