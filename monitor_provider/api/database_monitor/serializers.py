from flask_restplus import fields
from monitor_provider.api.restplus import api

database_monitor_cassandra_serializer = api.model('DatabaseMonitorCassandra', {
    'database_name': fields.String(required=True, description='Database Name', max_length=15),
    'port': fields.String(required=True, description='Port', max_length=200),
    'version': fields.String(required=True, description='Version', max_length=200),
    'username': fields.String(required=True, description='Username', max_length=200),
    'password': fields.String(required=True, description='Password', max_length=200),
    'environment': fields.String(required=False, description='Environment', max_length=200),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200),
})

database_monitor_postgresql_serializer = api.model('DatabaseMonitorPostgreSQL', {
    'database_name': fields.String(required=True, description='Service Name', max_length=15),
    'port': fields.String(required=True, description='Port', max_length=200),
    'version': fields.String(required=True, description='Version', max_length=200),
    'username': fields.String(required=True, description='Username', max_length=200),
    'password': fields.String(required=True, description='Password', max_length=200),
    'dns': fields.String(required=True, description='DNS', max_length=200),
    'topology': fields.String(required=True, description='Topology options are: POSTGRESQL_SINGLE, POSTGRESQL_STANDBY.', max_length=200),
    'environment': fields.String(required=False, description='Environment', max_length=200),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200),
})


database_monitor_postgresql_serializer = api.model('DatabaseMonitorPostgreSQL', {
    'database_name': fields.String(required=True, description='Service Name', max_length=15),
    'port': fields.String(required=True, description='Port', max_length=200),
    'version': fields.String(required=True, description='Version', max_length=200),
    'username': fields.String(required=True, description='Username', max_length=200),
    'password': fields.String(required=True, description='Password', max_length=200),
    'dns': fields.String(required=True, description='DNS', max_length=200),
    'topology': fields.String(required=True, description='Topology options are: POSTGRESQL_SINGLE, POSTGRESQL_STANDBY.', max_length=200),
    'environment': fields.String(required=False, description='Environment', max_length=200),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200),
})