from monitor_provider.credentials.base import CredentialBase, CredentialAdd


class CredentialDBMonitor(CredentialBase):

    @property
    def user(self):
        return self.content['user']

    @property
    def password(self):
        return self.content['password']

    @property
    def host(self):
        return self.content['host']

    @property
    def port(self):
        return self.content['port']

    @property
    def database(self):
        return self.content['database']

    @property
    def database_endpoint(self):
        return {
            "database": self.database,
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password
        }

    @property
    def default_cloud_name(self):
        return self.content['default_cloud_name']

    @property
    def default_organization_name(self):
        return self.content['default_organization_name']

    @property
    def default_machine_type(self):
        return self.content['default_machine_type']

    @property
    def default_environment(self):
        return self.content['default_environment']

    @property
    def decode_key(self):
        return self.content['decode_key']

class CredentialAddDBMonitor(CredentialAdd):

    @property
    def valid_fields(self):
        return [
            'user', 'password', 'host', 'port', 'database',
            'default_cloud_name', 'default_organization_name',
            'default_machine_type', 'default_environment', 'decode_key'
        ]
