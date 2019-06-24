from monitor_provider.credentials.dbmonitor import (
        CredentialDBMonitor, CredentialAddDBMonitor
    )
from monitor_provider.providers.base import ProviderBase


class ProviderDBMonitor(ProviderBase):

    @classmethod
    def get_provider(cls):
        return 'dbmonitor'

    def build_credential(self):
        return CredentialDBMonitor(self.provider, self.environment)

    def get_credential_add(self):
        return CredentialAddDBMonitor

