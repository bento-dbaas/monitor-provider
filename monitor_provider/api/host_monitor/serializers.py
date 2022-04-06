from flask_restplus import fields
from monitor_provider.api.restplus import api

host_monitor_dbmonitor_serializer = api.model('HostMonitorDbMonitor', {
    'host_name': fields.String(required=True, description='Host Name', max_length=200),
    'ip': fields.String(required=True, description='IP', max_length=200),
    'dns': fields.String(required=True, description='DNS', max_length=200),
    'so_name': fields.String(required=True, description='So Name', max_length=200),
    'service_name': fields.String(required=True, description='Service Name', max_length=200),
    'cpu': fields.String(required=False, description='CPU', max_length=200),
    'memory_mb': fields.String(required=False, description='Memory MB', max_length=200),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200),
})

host_monitor_zabbix_serializer = api.model('HostMonitorZabbix', {
    'host_name': fields.String(required=True, description='Host Name', max_length=200),
    'ip': fields.String(required=True, description='IP', max_length=200),
    'dns': fields.String(required=False, description='DNS', max_length=200),
    'so_name': fields.String(required=False, description='So Name', max_length=200),
    'service_name': fields.String(required=False, description='Service Name', max_length=200),
    'cpu': fields.String(required=False, description='CPU', max_length=200),
    'memory_mb': fields.String(required=False, description='Memory MB', max_length=200),
    'machine_type': fields.String(required=False, description='Machine Type', max_length=200),
    'organization_name': fields.String(required=False, description='Organization Name', max_length=200),
    'cloud_name': fields.String(required=False, description='Cloud Name', max_length=200),
})