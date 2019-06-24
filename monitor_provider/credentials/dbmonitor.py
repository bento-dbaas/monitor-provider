from monitor_provider.credentials.base import CredentialBase, CredentialAdd


class CredentialDBMonitor(CredentialBase):

    @property
    def user(self):
        return self.content['user']

    @property
    def password(self):
        return self.content['password']

    @property
    def endpoint(self):
        return self.content['endpoint']


class CredentialAddDBMonitor(CredentialAdd):

    @property
    def valid_fields(self):
        return [
            'user', 'password', 'endpoint'
        ]
