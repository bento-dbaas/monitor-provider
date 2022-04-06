from flask_restplus import fields
from monitor_provider.api.restplus import api

tcp_monitor_serializer = api.model('TcpMonitor', {
    'host': fields.String(required=True, description='Host', max_length=200),
    'port': fields.String(required=True, description='Port', max_length=200),
    'environment': fields.String(required=False, description='Environment', max_length=200),
    'locality': fields.String(required=False, description='Locality', max_length=200),
    'alarm': fields.String(required=False, description='Alarm', max_length=200),
    'doc': fields.String(required=False, description='Doc', max_length=200),
    'hostgroups': fields.String(required=False, description='Host Groups', max_length=200),
    'notes': fields.String(required=False, description='Notes', max_length=200),
    'notification_email': fields.String(required=False, description='Notification Email', max_length=200),
    'notification_slack': fields.String(required=False, description='Notification Slack', max_length=200),
    'zbx_proxy': fields.String(required=False, description='Zabix Proxy', max_length=200),
})
