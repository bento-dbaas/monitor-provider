from monitor_provider.credentials.base import CredentialBase, CredentialAdd


class CredentialZabbix(CredentialBase):

    @property
    def user(self):
        return self.content['user']

    @property
    def password(self):
        return self.content['password']

    @property
    def endpoint(self):
        return self.content['endpoint']

    @property
    def default_environment(self):
        return self.content['default_environment']

    @property
    def default_db_environment(self):
        return self.content['default_db_environment']

    @property
    def default_locality(self):
        return self.content['default_locality']

    @property
    def default_hostgroups(self):
        return self.content['default_hostgroups']

    @property
    def alarm(self):
        return self.content['alarm']


class CredentialAddZabbix(CredentialAdd):

    @property
    def valid_fields(self):
        return [
            'user', 'password', 'endpoint', 'alarm', 'default_environment',
            'default_db_environment', 'default_locality', 'default_hostgroups'
        ]
