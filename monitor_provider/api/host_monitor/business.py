import logging
import json
from monitor_provider.api.restplus import response_invalid_request, response_created, response_not_found, response_ok
from monitor_provider.providers import get_provider_to


def create_host_monitor(provider_name, env, data):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        host = provider.create_host_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=host.identifier)


def get_host_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    host = provider.get_host_monitor(identifier_or_name)
    if not host:
        return response_not_found(identifier_or_name)
    return response_ok(**host.get_json)


def delete_host_monitor(provider_name, env, identifier):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_host_monitor(identifier)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()
