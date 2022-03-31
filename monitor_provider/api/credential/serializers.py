from flask_restplus import fields
from monitor_provider.api.restplus import api

credential_serializer_dbmonitor = api.model('CredentialDBMonitor', {
    'user': fields.String(required=True, description='Ip', max_length=15),
    'password': fields.String(required=True, description='Name', max_length=200),
    'host': fields.String(required=True, description='Domain', max_length=150),
    'port': fields.String(required=True, description='Domain', max_length=150),
    'database': fields.String(required=True, description='Domain', max_length=150),
    'default_cloud_name': fields.String(required=True, description='Domain', max_length=150),
    'default_organization_name': fields.String(required=True, description='Domain', max_length=150),
    'default_machine_type': fields.String(required=True, description='Domain', max_length=150),
    'default_environment': fields.String(required=True, description='Domain', max_length=150),
    'decode_key': fields.String(required=True, description='Domain', max_length=150),
})

credential_serializer_zabbix = api.model('CredentialZabbix', {
    'user': fields.String(required=True, description='Ip', max_length=15),
    'password': fields.String(required=True, description='Name', max_length=200),
    'endpoint': fields.String(required=True, description='Domain', max_length=150),
    'default_environment': fields.String(required=True, description='Domain', max_length=150),
    'default_locality': fields.String(required=True, description='Domain', max_length=150),
    'default_hostgroups': fields.String(required=True, description='Domain', max_length=150),
    'alarm': fields.String(required=True, description='Domain', max_length=150),
})

# credential_serializer = api.model('CredentialBase', {
#     'user': fields.String(required=True, description='Ip', max_length=15),
#     'password': fields.String(required=True, description='Name', max_length=200),
# })
#
# credential_serializer_dbmonitor = api.inherit('CredentialDBMonitor', credential_serializer, {
#     'host': fields.String(required=True, description='Domain', max_length=150),
#     'port': fields.String(required=True, description='Domain', max_length=150),
#     'database': fields.String(required=True, description='Domain', max_length=150),
#     'default_cloud_name': fields.String(required=True, description='Domain', max_length=150),
#     'default_organization_name': fields.String(required=True, description='Domain', max_length=150),
#     'default_machine_type': fields.String(required=True, description='Domain', max_length=150),
#     'default_environment': fields.String(required=True, description='Domain', max_length=150),
#     'decode_key': fields.String(required=True, description='Domain', max_length=150),
# })
#
# credential_serializer_zabbix = api.inherit('CredentialZabbix', credential_serializer, {
#     'endpoint': fields.String(required=True, description='Domain', max_length=150),
#     'default_environment': fields.String(required=True, description='Domain', max_length=150),
#     'default_locality': fields.String(required=True, description='Domain', max_length=150),
#     'default_hostgroups': fields.String(required=True, description='Domain', max_length=150),
#     'alarm': fields.String(required=True, description='Domain', max_length=150),
# })
