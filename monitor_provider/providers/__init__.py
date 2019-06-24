from monitor_provider.providers.base import ProviderBase
from monitor_provider.providers.dbmonitor import ProviderDBMonitor
#from monitor_provider.providers.zabbix import ProviderZabbix


def get_provider_to(provider_name):
    for cls in ProviderBase.__subclasses__():
        if cls.get_provider() == provider_name:
            return cls

    raise NotImplementedError("No provider to '{}'".format(provider_name))
