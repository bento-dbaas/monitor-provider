import logging
import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.credential.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.credential.business import get_all_credentials, create_credential, get_credential, \
    delete_credential

ns = api.namespace('', description='Operations related to credential')


@ns.route('/<string:provider_name>/credentials')
class CredentialCollection(Resource):
    @api.response(200, "Dns successfully listed")
    @auth.login_required()
    def get(self, provider_name):
        """
        Return all registered credentials
        """
        return get_all_credentials(provider_name)


@ns.route('/dbmonitor/<string:env>/credential')
class CredentialDbmonitorItem(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(credential_serializer_dbmonitor)
    @auth.login_required()
    def post(self, provider_name, env):
        """
        Create new Credential for dbmonitor
        """
        data = json.loads(request.data or 'null')
        return create_credential(provider_name, env, data)

    @api.expect(credential_serializer_dbmonitor)
    @auth.login_required()
    def get(self, provider_name, env):
        """
        Return Credential of dbmonitor based on provider name and env
        """
        return get_credential(provider_name, env)

    @api.expect(credential_serializer_dbmonitor)
    @auth.login_required()
    def put(self):
        """
        Update Credential of dbmonitor based on provider name and env
        """
        return create_credential(provider_name, env)

    @api.expect(credential_serializer_dbmonitor)
    @auth.login_required()
    def delete(self):
        """
        Delete Credential of dbmonitor based on provider name and env
        """
        return delete_credential(provider_name, env)


@ns.route('/zabbix/<string:env>/credential')
class CredentialZabixItem(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(credential_serializer_zabbix)
    @auth.login_required()
    def post(self, env):
        """
        Create new Credential for zabix
        """
        provider_name = 'zabbix'
        return create_credential(provider_name, env)

    @auth.login_required()
    def get(self, provider_name, env):
        """
        Return Credential of zabix based on provider name and env
        """
        return get_credential(provider_name, env)

    @auth.login_required()
    def put(self):
        """
        Update Credential of zabix based on provider name and env
        """
        return create_credential(provider_name, env)

    @auth.login_required()
    def delete(self):
        """
        Delete Credential of zabix based on provider name and env
        """
        return delete_credential(provider_name, env)
