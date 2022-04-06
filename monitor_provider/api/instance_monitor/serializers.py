from flask_restplus import fields
from monitor_provider.api.restplus import api

instance_monitor_serializer = api.model('InstanceMonitor', {
    'dns': fields.String(required=True, description='DNS', max_length=15),
    'port': fields.String(required=True, description='Port', max_length=200),
    'instance_name': fields.String(required=True, description='Instance Name', max_length=200),
    'instance_type': fields.String(required=True, description='Instance Type - INSTANCIA_MONGODB / INSTANCIA_MONGODB_ARBITER', max_length=200),
    'database_name': fields.String(required=True, description='Database Name', max_length=200),
    'machine': fields.String(required=False, description='Machine', max_length=200),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200),
    'disk_path': fields.String(required=False, description='Disk Path', max_length=200),
})
