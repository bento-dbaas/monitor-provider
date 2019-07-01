from monitor_provider.credentials.dbmonitor import (
        CredentialDBMonitor, CredentialAddDBMonitor
    )
from monitor_provider.providers.base import ProviderBase
from monitor_provider.models.dbmonitor import DbmonitorHandleModels

class ProviderDBMonitor(ProviderBase):

    @classmethod
    def get_provider(cls):
        return 'dbmonitor'

    def build_credential(self):
        return CredentialDBMonitor(self.provider, self.environment)

    def get_credential_add(self):
        return CredentialAddDBMonitor

    def register_host(self, **kwargs):
        dbhandle = DbmonitorHandleModels(self.credential.database_endpoint)
        return dbhandle.register_host(self.credential, **kwargs)

    def get_host(self, host_name):
        dbhandle = DbmonitorHandleModels(self.credential.database_endpoint)
        return dbhandle.get_host(host_name)

    def delete_host(self, host_id):
        dbhandle = DbmonitorHandleModels(self.credential.database_endpoint)
        dbhandle.delete_host(host_id)

    def get_service(self, service_name):
        dbhandle = DbmonitorHandleModels(self.credential.database_endpoint)
        return dbhandle.get_service(service_name)

    def register_service(self, **kwargs):
        dbhandle = DbmonitorHandleModels(self.credential.database_endpoint)
        return dbhandle.register_service(self.credential, **kwargs)

    def delete_service(self, service_id):
        dbhandle = DbmonitorHandleModels(self.credential.database_endpoint)
        dbhandle.delete_service(service_id)
