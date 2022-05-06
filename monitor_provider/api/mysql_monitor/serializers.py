from flask_restplus import fields
from monitor_provider.api.restplus import api

mysql_monitor_serializer = api.model('MysqlMonitor', {
    'host': fields.String(required=True, description='Host', max_length=200, example='string'),
    'port': fields.String(required=True, description='Port', max_length=200, example='string'),
    'version': fields.String(required=True, description='Version', max_length=200, example='string'),
    'environment': fields.String(required=False, description='Environment', max_length=200, example='string'),
    'locality': fields.String(required=False, description='Locality', max_length=200, example='string'),
    'alarm': fields.String(required=False, description='Alarm', max_length=200, example='string'),
    'hostgroups': fields.String(required=False, description='Host Groups', max_length=200, example='string'),
    'user': fields.String(required=False, description='User', max_length=200, example='string'),
    'password': fields.String(required=False, description='Password', max_length=200, example='string'),
    'healthcheck': fields.String(required=False, description='healthcheck is an optional boolean field. To enable it '
                                                             'just pass it along with data as "healthcheck": true',
                                 max_length=200, example='string'),
})
