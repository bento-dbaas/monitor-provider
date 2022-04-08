from flask_restplus import fields
from monitor_provider.api.restplus import api

service_monitor_serializer = api.model('ServiceMonitor', {
    'service_name': fields.String(required=True, description='Service Name', max_length=200),
    'url': fields.String(required=False, description='URL', max_length=200),
})
