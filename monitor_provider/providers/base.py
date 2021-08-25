from mongoengine.queryset.visitor import Q

from monitor_provider.models.models import (
    ServiceMonitor,
    HostMonitor,
    WebMonitor,
    DatabaseCassandraMonitor,
    InstanceCassandraMonitor)


class ProviderBase(object):

    def __init__(self, environment):
        self.environment = environment
        self._credential = None

    @property
    def credential(self):
        if not self._credential:
            self._credential = self.build_credential()
        return self._credential

    def credential_add(self, content):
        credential_cls = self.get_credential_add()
        credential = credential_cls(self.provider, self.environment, content)
        is_valid, error = credential.is_valid()
        if not is_valid:
            return False, error

        try:
            insert = credential.save()
        except Exception as e:
            return False, str(e)
        else:
            return True, insert.get('_id')

    @property
    def provider(self):
        return self.get_provider()

    @classmethod
    def get_provider(cls):
        raise NotImplementedError

    def build_credential(self):
        raise NotImplementedError

    def get_credential_add(self):
        raise NotImplementedError

    def check_mandatory_fields(self, mandatory_fields, **data):
        for mandatory_field in mandatory_fields:
            item = data.get(mandatory_field, None)
            if not item:
                raise Exception("{} is mandatory".format(mandatory_field))

    def _create_service_monitor(self, service, **kwargs):
        raise NotImplementedError

    def create_service_monitor(self, **kwargs):
        mandatory_fields = ['service_name']
        self.check_mandatory_fields(mandatory_fields, **kwargs)
        service_name = kwargs.get("service_name")

        service = ServiceMonitor()
        service.monitor_provider = self.provider
        service.monitor_environment = self.environment
        service.service_name = service_name
        self._create_service_monitor(service, **kwargs)

        service.save()
        return service

    def get_database_cassandra_monitor(self, identifier_or_name):
        try:
            return DatabaseCassandraMonitor.objects(
                Q(identifier=identifier_or_name) | Q(database_name=identifier_or_name),
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except DatabaseCassandraMonitor.DoesNotExist:
            return None

    def _create_database_cassandra_monitor(self, cassandra, **kwargs):
        raise NotImplementedError

    def create_database_cassandra_monitor(self, **kwargs):
        mandatory_fields = ['database_name', 'type', 'port', 'version', 'username', 'password', 'cloud_name']
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        database_name = kwargs.get('database_name')
        if self.get_database_cassandra_monitor(database_name):
            raise Exception(
                "A database named '{}' already exists".format(database_name)
            )

        cassandra = DatabaseCassandraMonitor()
        cassandra.monitor_provider = self.provider
        cassandra.monitor_environment = self.environment
        cassandra.database_name = database_name
        cassandra.port = kwargs.get('port')
        cassandra.type = kwargs.get('type')
        cassandra.username = kwargs.get('username')
        cassandra.version = kwargs.get('version')
        cassandra.active = True
        self._create_database_cassandra_monitor(cassandra, **kwargs)

        cassandra.save()
        return cassandra

    def _delete_database_cassandra_monitor(self, cassandra):
        raise NotImplementedError

    def delete_database_cassandra_monitor(self, identifier):
        cassandra = DatabaseCassandraMonitor.objects(
            identifier=identifier,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_database_cassandra_monitor(cassandra)
        cassandra.delete()

    def get_instance_cassandra_monitor(self, identifier_or_name):
        try:
            return InstanceCassandraMonitor.objects(
                Q(identifier=identifier_or_name) | Q(instance_name=identifier_or_name),
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except InstanceCassandraMonitor.DoesNotExist:
            return None

    def _create_instance_cassandra_monitor(self, instance, **kwargs):
        raise NotImplementedError

    def create_instance_cassandra_monitor(self, **kwargs):
        mandatory_fields = ['instance_name', 'machine_type', 'dns', 'port', 'disk_path', 'database_name']
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        database = self.get_database_cassandra_monitor(identifier_or_name=kwargs.get('database_name'))
        if database is None:
            raise Exception(
                "A database named '{}' could not be found".format(kwargs.get('database_name'))
            )

        instance_name = kwargs.get('instance_name')
        if self.get_instance_cassandra_monitor(instance_name):
            raise Exception(
                "A instance named '{}' already exists".format(instance_name)
            )

        instance = InstanceCassandraMonitor()
        instance.monitor_provider = self.provider
        instance.monitor_environment = self.environment
        instance.instance_name = instance_name
        instance.database_id = database.identifier
        instance.port = kwargs.get('port')
        instance.dns = kwargs.get('dns')
        instance.machine_type = kwargs.get('machine_type')
        instance.machine = kwargs.get('machine')
        instance.disk_path = kwargs.get('disk_path')
        instance.active = True
        self._create_instance_cassandra_monitor(instance, **kwargs)

        instance.save()
        return instance

    def _delete_instance_cassandra_monitor(self, identifier):
        raise NotImplementedError

    def delete_instance_cassandra_monitor(self, instance_name):
        instance = InstanceCassandraMonitor.objects(
            instance_name=instance_name,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_instance_cassandra_monitor(instance)
        instance.delete()

    def get_service_monitor(self, identifier_or_name):
        try:
            return ServiceMonitor.objects(
                identifier=identifier_or_name,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except ServiceMonitor.DoesNotExist:
            pass
        try:
            return ServiceMonitor.objects(
                service_name=identifier_or_name,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except ServiceMonitor.DoesNotExist:
            return None

    def _delete_service_monitor(self, service):
        raise NotImplementedError

    def delete_service_monitor(self, identifier):
        service = ServiceMonitor.objects(
            identifier=identifier,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_service_monitor(service)
        service.delete()

    def _create_host_monitor(self, host, **kwargs):
        raise NotImplementedError

    def create_host_monitor(self, **kwargs):
        mandatory_fields = ['host_name', 'ip']
        self.check_mandatory_fields(mandatory_fields, **kwargs)
        host_name = kwargs.get("host_name")
        ip = kwargs.get("ip")

        host = HostMonitor()
        host.monitor_provider = self.provider
        host.monitor_environment = self.environment
        host.host_name = host_name
        host.ip = ip

        self._create_host_monitor(host, **kwargs)

        host.save()
        return host

    def get_host_monitor(self, identifier_or_name):
        try:
            return HostMonitor.objects(
                identifier=identifier_or_name,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except HostMonitor.DoesNotExist:
            pass
        try:
            return HostMonitor.objects(
                host_name=identifier_or_name,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except HostMonitor.DoesNotExist:
            return None

    def _delete_host_monitor(self, host):
        raise NotImplementedError

    def delete_host_monitor(self, identifier):
        host = HostMonitor.objects(
            identifier=identifier,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_host_monitor(host)
        host.delete()

    def _create_web_monitor(self, web, **kwargs):
        raise NotImplementedError

    def create_web_monitor(self, **kwargs):
        mandatory_fields = ['host_name']
        self.check_mandatory_fields(mandatory_fields, **kwargs)
        host_name = kwargs.get("host_name")

        web = WebMonitor()
        web.monitor_provider = self.provider
        web.monitor_environment = self.environment
        web.host_name = host_name

        self._create_web_monitor(web, **kwargs)

        web.save()
        return web


    def get_web_monitor(self, identifier):
        try:
            return WebMonitor.objects(
                identifier=identifier,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except WebMonitor.DoesNotExist:
            return None

    def _delete_web_monitor(self, web):
        raise NotImplementedError

    def delete_web_monitor(self, identifier):
        host = WebMonitor.objects(
            identifier=identifier,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_web_monitor(host)
        host.delete()
