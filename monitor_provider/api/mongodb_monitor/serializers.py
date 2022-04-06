from flask_restplus import fields
from monitor_provider.api.restplus import api

mongodb_monitor_serializer = api.model('MongoDbMonitor', {
    'host': fields.String(required=True, description='Host', max_length=200),
    'port': fields.String(required=True, description='Port', max_length=200),
    'mongo_version': fields.String(required=True, description='Mongo Versions: "3.0", "3.4", "4.0", "4.2"',
                                   max_length=5),
    'environment': fields.String(required=False, description='Environment', max_length=200),
    'locality': fields.String(required=False, description='Locality', max_length=200),
    'alarm': fields.String(required=False, description='Alarm', max_length=200),
    'hostgroups': fields.String(required=False, description='Host Groups', max_length=200),
    'user': fields.String(required=False, description='User', max_length=200),
    'password': fields.String(required=False, description='Password', max_length=200),
    'replicaset': fields.String(required=False, description='Allowed Values: 0, 1. Default Value: 0.',
                                max_length=2),
})
