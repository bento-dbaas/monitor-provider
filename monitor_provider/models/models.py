from mongoengine import Document, StringField, IntField


class ServiceMonitor(Document):
    provider = StringField(required=True)
    identifier = StringField(required=True)
    name = StringField(required=True)
    environment = StringField(required=False)
    environment_id = StringField(required=False)
    url = StringField(required=False)

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        return {
            'provider': self.provider,
            'identifier': self.identifier,
            'name': self.name,
            'environment': self.environment,
            'environment_id': self.environment_id,
            'url': self.url,
        }


class HostMonitor(Document):
    provider = StringField(required=True)
    identifier = StringField(required=True)
    name = StringField(required=True)
    ip = StringField(required=True)
    dns = StringField(required=False)
    so_name = StringField(required=False)
    cpu = IntField(required=False)
    memory_mb = IntField(required=False)
    organization_name= StringField(required=False)
    organization_id = IntField(required=False)
    cloud_name = StringField(required=False)
    cloud_id = IntField(required=False)
    machine_type = StringField(required=False)
    machine_type_id = StringField(required=False)
    service_name = StringField(required=False)
    service_id = IntField(required=False)

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        return {
            'provider': self.provider,
            'identifier': self.identifier,
            'name': self.name,
            'dns': self.dns,
            'ip': self.ip,
            'cpu': self.cpu,
            'so_name': self.so_name,
            'memory_mb': self.memory_mb,
            'organization_name': self.organization_name,
            'machine_type': self.machine_type,
            'service_name': self.service_name,
        }


