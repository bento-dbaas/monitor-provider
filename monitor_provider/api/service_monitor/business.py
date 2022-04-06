from monitor_provider.api.restplus import response_invalid_request, response_created, response_not_found, response_ok
from monitor_provider.providers import get_provider_to
from traceback import print_exc


def create_service_monitor(provider_name, env, data):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        service = provider.create_service_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=service.identifier)


def get_service_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    service = provider.get_service_monitor(identifier_or_name)
    if not service:
        return response_not_found(identifier_or_name)
    return response_ok(**service.get_json)


def delete_service_monitor(provider_name, env, identifier):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_service_monitor(identifier)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()
