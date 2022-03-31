import logging
import json
from monitor_provider.api.restplus import response_invalid_request, response_created, response_not_found, response_ok
from monitor_provider.providers import get_provider_to


def create_tcp_monitor(provider_name, env, data):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        tcp = provider.create_tcp_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=tcp.identifier)


def get_tcp_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    tcp = provider.get_tcp_monitor(identifier_or_name)
    if not tcp:
        return response_not_found(identifier_or_name)
    return response_ok(**tcp.get_json)


def delete_tcp_monitor(provider_name, env, identifier):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_tcp_monitor(identifier)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()