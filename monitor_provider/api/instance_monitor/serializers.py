from flask_restplus import fields
from monitor_provider.api.restplus import api

instance_monitor_serializer = api.model('InstanceMonitor', {
    'dns': fields.String(required=True, description='DNS', max_length=200, example='string'),
    'port': fields.String(required=True, description='Port', max_length=200, example='string'),
    'instance_name': fields.String(required=True, description='Instance Name', max_length=200, example='string'),
    'database_name': fields.String(required=True, description='Database Name', max_length=200, example='string'),
    'instance_type': fields.String(required=False, description='Instance Type - Required when database '
                                                              'is mongodb - types: '
                                                              'INSTANCIA_MONGODB / INSTANCIA_MONGODB_ARBITER',
                                   max_length=200, example='string'),
    'machine': fields.String(required=False, description='Machine', max_length=200, example='string'),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200, example='string'),
    'disk_path': fields.String(required=False, description='Disk Path', max_length=200, example='string'),
})
