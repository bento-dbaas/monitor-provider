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

    def _create_host_monitor(self, host, **kwargs):
        data = {
            'host': host.name,
            'ip': host.ip,
            'environment': self.credential.default_environment,
            'locality': self.credential.default_locality,
            'hostgroups': self.credential.default_hostgroups,
            'alarm': self.credential.alarm
        }
        host.identifier = host.name
        self.zapi.globo.createLinuxMonitors(**data)

    def _delete_host_monitor(self, host):
        data = {'host': host.identifier}
        self.zapi.globo.deleteMonitors(**data)

