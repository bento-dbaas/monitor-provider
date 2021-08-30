from mongoengine import Document, StringField, IntField, BooleanField


class ServiceMonitor(Document):
    monitor_provider = StringField(required=True)
    monitor_environment = StringField(required=True)
    identifier = StringField(required=True)
    service_name = StringField(required=True)
    environment = StringField(required=False)
    environment_id = StringField(required=False)
    url = StringField(required=False)

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        d = {
            'monitor_provider': self.monitor_provider,
            'monitor_environment': self.monitor_environment,
            'identifier': self.identifier,
            'service_name': self.service_name,
            'environment': self.environment,
            'environment_id': self.environment_id,
            'url': self.url,
        }
        return {k: v for k, v in d.items() if v}


class DatabaseCassandraMonitor(Document):
    monitor_provider = StringField(required=True)
    monitor_environment = StringField(required=True)
    active = BooleanField(required=True)
    identifier = StringField(required=True)
    environment = StringField(required=False)
    environment_id = StringField(required=False)
    database_name = StringField(required=False)
    type = StringField(required=False)
    port = IntField(required=False)
    version = StringField(required=False)
    sgbd = StringField()
    sgbd_type_id = StringField()
    topology_type_id = IntField()
    topology_name = StringField()
    dns = StringField(required=False)
    machine = StringField()
    machine_type = StringField(required=False)
    machine_type_id = StringField(required=False)
    username = StringField(required=True)
    cloud_name = StringField(required=False)
    cloud_id = IntField(required=False)

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        d = {
            'cloud': self.cloud_name,
            'dns': self.dns,
            'nome': self.database_name,
            'port': self.port,
            'sgbd': self.sgbd,
            'topology': self.topology_name,
            'type': self.type,
            'machine_type': self.machine_type,
            'version': self.version,
        }
        return {k: v for k, v in d.items() if v}


class InstanceCassandraMonitor(Document):
    monitor_provider = StringField(required=True)
    monitor_environment = StringField(required=True)
    identifier = StringField(required=True)
    database_id = IntField()
    instance_name = StringField()
    database_name = StringField()
    machine_type = StringField(required=False)
    machine_type_id = StringField(required=False)
    dns = StringField()
    port = StringField()
    active = BooleanField(default=True)
    type_mongodb = StringField()
    disk_path = StringField()
    type_instance = IntField()

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        d = {
            'database_name': self.database_name,
            'dns': self.dns,
            'instance_name': self.instance_name,
            'machine_type': self.machine_type,
            'type_instance': self.type_instance,
        }
        return {k: v for k, v in d.items() if v}


class HostMonitor(Document):
    monitor_provider = StringField(required=True)
    monitor_environment = StringField(required=True)
    identifier = StringField(required=True)
    host_name = StringField(required=True)
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
    environment = StringField(required=False)
    locality = StringField(required=False)
    hostgroups = StringField(required=False)
    alarm = StringField(required=False)

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        d = {
            'monitor_provider': self.monitor_provider,
            'monitor_environment': self.monitor_environment,
            'identifier': self.identifier,
            'host_name': self.host_name,
            'dns': self.dns,
            'ip': self.ip,
            'cpu': self.cpu,
            'so_name': self.so_name,
            'memory_mb': self.memory_mb,
            'organization_name': self.organization_name,
            'machine_type': self.machine_type,
            'service_name': self.service_name,
            'environment': self.environment,
            'locality': self.locality,
            'hostgroups': self.hostgroups,
            'alarm': self.alarm,
        }
        return {k: v for k, v in d.items() if v}


class WebMonitor(Document):
    monitor_provider = StringField(required=True)
    monitor_environment = StringField(required=True)
    identifier = StringField(required=True)
    host = StringField(required=True)
    environment = StringField(required=False)
    locality = StringField(required=False)
    url = StringField(required=False)
    hostgroups = StringField(required=False)
    required_string = StringField(required=False)
    alarm = StringField(required=False)

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        d = {
            'monitor_provider': self.monitor_provider,
            'monitor_environment': self.monitor_environment,
            'identifier': self.identifier,
            'host': self.host,
            'environment': self.environment,
            'locality': self.locality,
            'url': self.url,
            'hostgroups': self.hostgroups,
            'required_string': self.required_string,
            'alarm': self.alarm
        }
        return {k: v for k, v in d.items() if v}


class TcpMonitor(Document):
    monitor_provider = StringField(required=True)
    monitor_environment = StringField(required=True)
    identifier = StringField(required=True)
    host = StringField(required=True)
    port = StringField(required=True)
    locality = StringField(required=True)
    alarm = StringField(required=False)
    hostgroups = StringField(required=False)

    @property
    def uuid(self):
        return str(self.pk)

    @property
    def get_json(self):
        d = {
            'monitor_provider': self.monitor_provider,
            'monitor_environment': self.monitor_environment,
            'identifier': self.identifier,
            'host': self.host,
            'port': self.port,
            'locality': self.locality,
            'alarm': self.alarm,
            'hostgroups': self.hostgroups
        }
        return {k: v for k, v in d.items() if v}
