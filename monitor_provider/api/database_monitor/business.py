import logging
import json
from monitor_provider.providers.constants import VALID_DBMS
from monitor_provider.api.restplus import response_invalid_request, response_created, response_not_found, response_ok, \
    _response
from monitor_provider.providers import get_provider_to
from traceback import print_exc


def create_database_monitor(provider_name, env, dbms, data):
    if dbms not in VALID_DBMS:
        return response_invalid_request(
            'Invalid database. Available options are {}'.format(list(VALID_DBMS))
        )
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        monitor = provider.create_database_monitor(dbms_name=dbms, **data)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    return response_created(success=True, identifier=monitor.identifier)


def get_database_monitor(provider_name, env, identifier_or_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))

    database = provider.get_database_monitor(identifier_or_name)
    if not database:
        return response_not_found(identifier_or_name)
    return response_ok(**database.get_json)


def delete_database_monitor(provider_name, env, database_name):
    try:
        provider_cls = get_provider_to(provider_name)
        provider = provider_cls(env)
        provider.delete_database_monitor(database_name)
    except Exception as e:
        print_exc()
        return response_invalid_request(str(e))
    return response_ok()
