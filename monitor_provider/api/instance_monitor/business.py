from monitor_provider.providers.constants import VALID_DBMS
from monitor_provider.api.restplus import response_invalid_request, response_created, response_not_found, response_ok
from monitor_provider.providers import get_provider_to
from traceback import print_exc


def create_instance_monitor(provider_name, env, dbms, data):
    if dbms not in VALID_DBMS:
        return response_invalid_request(
            'Invalid database. Available options are {}'.format(list(VALID_DBMS))
        )
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        monitor = provider.create_instance_monitor(dbms_name=dbms, **data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_created(success=True, identifier=monitor.identifier)


def get_instance_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    database = provider.get_instance_monitor(identifier_or_name)
    if not database:
        return response_not_found(identifier_or_name)
    return response_ok(**database.get_json)


def delete_instance_monitor(provider_name, env, instance_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_instance_monitor(instance_name)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()