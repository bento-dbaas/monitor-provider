from flask_restplus import fields
from monitor_provider.api.restplus import api

web_monitor_serializer = api.model('WebMonitor', {
    'host_name': fields.String(required=True, description='Service Name', max_length=15),
    'url': fields.String(required=False, description='URL', max_length=200),
    'required_string': fields.String(required=False, description='URL', max_length=200),
})
