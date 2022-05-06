from flask_restplus import fields
from monitor_provider.api.restplus import api

credential_serializer_dbmonitor = api.model('CredentialDBMonitor', {
    'user': fields.String(required=True, description='Ip', max_length=200, example='string'),
    'password': fields.String(required=True, description='Name', max_length=200, example='string'),
    'host': fields.String(required=True, description='Host', max_length=200, example='string'),
    'port': fields.String(required=True, description='Port', max_length=200, example='string'),
    'database': fields.String(required=True, description='Database', max_length=200, example='string'),
    'default_cloud_name': fields.String(required=True, description='Default Cloud Name', max_length=200,
                                        example='string'),
    'default_organization_name': fields.String(required=True, description='Default Organization Name', max_length=200,
                                               example='string'),
    'default_machine_type': fields.String(required=True, description='Default Machine Type', max_length=200,
                                          example='string'),
    'default_environment': fields.String(required=True, description='Default Environment', max_length=200,
                                         example='string'),
    'decode_key': fields.String(required=True, description='Decode Key', max_length=200, example='string'),
})

credential_serializer_zabbix = api.model('CredentialZabbix', {
    'user': fields.String(required=True, description='Ip', max_length=200, example='string'),
    'password': fields.String(required=True, description='Name', max_length=200, example='string'),
    'endpoint': fields.String(required=True, description='Endpoint', max_length=200, example='string'),
    'default_environment': fields.String(required=True, description='Default Environment', max_length=200,
                                         example='string'),
    'default_db_environment': fields.String(required=True, description='Default Database Environment', max_length=200,
                                            example='string'),
    'default_locality': fields.String(required=True, description='Default Locality', max_length=200, example='string'),
    'default_hostgroups': fields.String(required=True, description='Default HostGroups', max_length=200,
                                        example='string'),
    'alarm': fields.String(required=True, description='Alarm', max_length=200, example='string'),
    'mysql_user': fields.String(required=True, description='MySQL User', max_length=200, example='string'),
    'mysql_password': fields.String(required=True, description='MySQL Password', max_length=200, example='string'),
    'mongodb_user': fields.String(required=True, description='MongoDB User', max_length=200, example='string'),
    'mongo_password': fields.String(required=True, description='MongoDB Password', max_length=200, example='string'),
})
