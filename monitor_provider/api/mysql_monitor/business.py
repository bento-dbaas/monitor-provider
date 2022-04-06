from monitor_provider.api.restplus import response_invalid_request, response_created, response_not_found, response_ok
from monitor_provider.providers import get_provider_to
from traceback import print_exc


def create_mysql_monitor(provider_name, env, data):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        db = provider.create_mysql_monitor(**data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=db.identifier)


def get_mysql_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    db = provider.get_mysql_monitor(identifier_or_name)
    if not db:
        return response_not_found(identifier_or_name)
    return response_ok(**db.get_json)


def delete_mysql_monitor(provider_name, env, identifier):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_mysql_monitor(identifier)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()
