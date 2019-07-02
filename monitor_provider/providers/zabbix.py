from pyzabbix import ZabbixAPI
from monitor_provider.credentials.zabbix import (
        CredentialZabbix, CredentialAddZabbix
    )
from monitor_provider.providers.base import ProviderBase

class ProviderZabbix(ProviderBase):

    def __init__(self, environment):
        self._zapi = None
        super(ProviderZabbix, self).__init__(environment)

    @classmethod
    def get_provider(cls):
        return 'zabbix'

    def build_credential(self):
        return CredentialZabbix(self.provider, self.environment)

    def get_credential_add(self):
        return CredentialAddZabbix

    @property
    def zapi(self):
        if not self._zapi:
            self._zapi = ZabbixAPI(self.credential.endpoint)
            self._zapi.login(self.credential.user, self.credential.password)
        return self._zapi

    def create_host(self, **kwargs):
        mandatory_fields = ['name', 'ip']
        self.check_mandatory_fields(mandatory_fields, **kwargs)
        data = {
            'host': kwargs.get("name"),
            'ip': kwargs.get("ip"),
            'environment': self.credential.default_environment,
            'locality': self.credential.default_locality,
            'hostgroups': self.credential.default_hostgroups,
            'alarm': self.credential.alarm
        }

        self.zapi.globo.createLinuxMonitors(**data)

        return 1


    def delete_host(self, host_name):
        data = {'host': host_name}
        self.zapi.globo.deleteMonitors(**data)

