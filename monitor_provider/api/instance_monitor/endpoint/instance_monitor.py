import json
from flask import request
from flask_restplus import Resource
from monitor_provider.api.instance_monitor.serializers import *
from monitor_provider.api.restplus import api, auth
from monitor_provider.api.instance_monitor.business import create_instance_monitor, get_instance_monitor, \
    delete_instance_monitor

ns = api.namespace('', description='Operations related to service_monitor')


@ns.route('/<string:provider_name>/<string:env>/instance/<string:dbms>/new')
class InstanceMonitorCreate(Resource):
    @api.response(201, "Credential successfully created")
    @api.expect(instance_monitor_serializer)
    @auth.login_required()
    def post(self, provider_name, env, dbms):
        """
        Create new Instance Monitor based on provider_name, env, dbms
        """
        data = json.loads(request.data or 'null')
        return create_instance_monitor(provider_name, env, dbms, data)


@ns.route('/<string:provider_name>/<string:env>/instance/<string:identifier_or_name>')
class InstanceMonitorItemGet(Resource):
    @auth.login_required()
    def get(self, provider_name, env, identifier_or_name):
        """
        Return Instance Monitor based on provider_name, env, identifier
        """
        return get_instance_monitor(provider_name, env, identifier_or_name)


@ns.route('/<string:provider_name>/<string:env>/instance/<string:instance_name>')
class InstanceMonitorItemDelete(Resource):
    @auth.login_required()
    def delete(self, provider_name, env, instance_name):
        """
        Delete Instance Monitor based on provider_name, env, instance_name
        """
        return delete_instance_monitor(provider_name, env, instance_name)
