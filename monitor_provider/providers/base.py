from mongoengine.queryset.visitor import Q

from monitor_provider.providers import constants
from monitor_provider.models.models import (
    ServiceMonitor,
    HostMonitor,
    MysqlMonitor,
    TcpMonitor,
    WebMonitor,
    DatabaseMonitor,
    InstanceMonitor,
    MongoDbMonitor)


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

    def get_database_monitor(self, identifier_or_name, raise_on_failure=False):
        try:
            return DatabaseMonitor.objects(
                Q(identifier=identifier_or_name) | Q(database_name=identifier_or_name),
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except DatabaseMonitor.DoesNotExist as exc:
            if raise_on_failure:
                raise Exception(exc)

            return None

    def _create_database_monitor(self, dbms, dbms_name, **kwargs):
        raise NotImplementedError

    def create_database_monitor(self, dbms_name, **kwargs):
        mandatory_fields = constants.MANDATORY_FIELDS[dbms_name]
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        database_name = kwargs.get('database_name')
        if self.get_database_monitor(database_name):
            raise Exception(
                "A database named '{}' already exists".format(database_name)
            )

        dbms = DatabaseMonitor()
        dbms.monitor_provider = self.provider
        dbms.monitor_environment = self.environment
        dbms.database_name = database_name
        dbms.port = kwargs.get('port')
        dbms.username = kwargs.get('username')
        dbms.version = kwargs.get('version')
        dbms.dns = kwargs.get('dns')
        dbms.active = True
        dbms.environment = kwargs.get('environment')
        dbms.cloud_name = kwargs.get('cloud_name')
        dbms.machine_type = kwargs.get('machine_type')
        dbms.machine = kwargs.get('machine')
        self._create_database_monitor(dbms, dbms_name, **kwargs)

        dbms.save()
        return dbms

    def _delete_database_monitor(self, sgbd):
        raise NotImplementedError

    def delete_database_monitor(self, database_name):
        sgbd = self.get_database_monitor(
            database_name,
            raise_on_failure=True
        )
        self._delete_database_monitor(sgbd)
        sgbd.delete()

    def get_instance_monitor(self, identifier_or_name, raise_on_failure=False):
        try:
            return InstanceMonitor.objects(
                Q(identifier=identifier_or_name) | Q(instance_name=identifier_or_name),
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except InstanceMonitor.DoesNotExist as exc:
            if raise_on_failure:
                raise Exception(exc)

            return None

    def _create_instance_monitor(self, instance, update_dns=False, **kwargs):
        raise NotImplementedError

    def create_instance_monitor(self, dbms_name, update_dns=False, **kwargs):
        mandatory_fields = ['instance_name', 'dns', 'port', 'database_name']
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        database = self.get_database_monitor(identifier_or_name=kwargs.get('database_name'))
        if database is None:
            raise Exception(
                "A database named '{}' could not be found".format(kwargs.get('database_name'))
            )

        instance_name = kwargs.get('instance_name')
        if self.get_instance_monitor(instance_name):
            raise Exception(
                "A instance named '{}' already exists".format(instance_name)
            )

        instance_type = kwargs.get('instance_type')
        if not instance_type:
            try:
                if dbms_name == constants.MONGODB:
                    raise KeyError
                else:
                    instance_type = constants.INSTANCIA[database.topology_type_id]
            except KeyError:
                raise Exception("An instance_type is mandatory")

        if dbms_name == constants.CASSANDRA:
            update_dns = True

        if dbms_name == constants.MONGODB:
            instance_type = constants.INSTANCIA_CHOICES[instance_type]

        instance = InstanceMonitor()
        instance.monitor_provider = self.provider
        instance.monitor_environment = self.environment
        instance.instance_name = instance_name
        instance.database_id = database.identifier
        instance.port = kwargs.get('port')
        instance.dns = kwargs.get('dns')
        instance.type_instance = instance_type
        instance.machine = kwargs.get('machine')
        instance.machine_type = kwargs.get('machine_type')
        instance.disk_path = kwargs.get('disk_path')
        instance.active = True
        self._create_instance_monitor(instance, update_dns=update_dns, **kwargs)

        instance.save()
        return instance

    def _delete_instance_monitor(self, identifier):
        raise NotImplementedError

    def delete_instance_monitor(self, instance_name):
        instance = self.get_instance_monitor(
            instance_name,
            raise_on_failure=True
        )
        self._delete_instance_monitor(instance)
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

    def _create_tcp_monitor(self, tcp, **kwargs):
        raise NotImplementedError

    def create_tcp_monitor(self, **kwargs):
        mandatory_fields = ["host", "port"]
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        tcp = TcpMonitor()
        tcp.monitor_provider = self.provider
        tcp.monitor_environment = self.environment
        tcp.host = kwargs.get("host")
        tcp.port = kwargs.get("port")
        tcp.environment = kwargs.get("environment")
        tcp.locality = kwargs.get("locality")
        tcp.alarm = kwargs.get("alarm")
        tcp.doc = kwargs.get("doc")
        tcp.hostgroups = kwargs.get("hostgroups")
        tcp.notes = kwargs.get("notes")
        tcp.notification_email = kwargs.get("notification_email")
        tcp.notification_slack = kwargs.get("notification_slack")
        tcp.zbx_proxy = kwargs.get("zbx_proxy")

        self._create_tcp_monitor(tcp, **kwargs)

        tcp.save()
        return tcp

    def _delete_tcp_monitor(self, tcp):
        raise NotImplementedError

    def delete_tcp_monitor(self, identifier):
        tcp = TcpMonitor.objects(
            identifier=identifier,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_tcp_monitor(tcp)
        tcp.delete()

    def get_tcp_monitor(self, identifier_or_name):
        try:
            return TcpMonitor.objects(
                identifier=identifier_or_name,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except TcpMonitor.DoesNotExist:
            return None

    def _create_mysql_monitor(self, db, **kwargs):
        raise NotImplementedError

    def create_mysql_monitor(self, **kwargs):
        mandatory_fields = ["host", "port", "version"]
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        db = MysqlMonitor()
        db.monitor_provider = self.provider
        db.monitor_environment = self.environment
        db.host = kwargs.get("host")
        db.port = kwargs.get("port")
        db.user = kwargs.get("user")
        db.environment = kwargs.get("environment")
        db.locality = kwargs.get("locality")
        db.alarm = kwargs.get("alarm")
        db.hostgroups = kwargs.get("hostgroups")
        db.version = kwargs.get("version")

        self._create_mysql_monitor(db, **kwargs)

        db.save()
        return db

    def _delete_mysql_monitor(self, db):
        raise NotImplementedError

    def delete_mysql_monitor(self, identifier):
        db = MysqlMonitor.objects(
            identifier=identifier,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_mysql_monitor(db)
        db.delete()

    def get_mysql_monitor(self, identifier_or_name):
        try:
            return MysqlMonitor.objects(
                identifier=identifier_or_name,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except MysqlMonitor.DoesNotExist:
            return None

    def _create_mongodb_monitor(self, db, **kwargs):
        raise NotImplementedError

    def create_mongodb_monitor(self, **kwargs):
        mandatory_fields = ["host", "port", "mongo_version"]
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        db = MongoDbMonitor()
        db.monitor_provider = self.provider
        db.monitor_environment = self.environment
        db.host = kwargs.get("host")
        db.port = kwargs.get("port")
        db.user = kwargs.get("user")
        db.environment = kwargs.get("environment")
        db.locality = kwargs.get("locality")
        db.alarm = kwargs.get("alarm")
        db.hostgroups = kwargs.get("hostgroups")
        db.mongo_version = kwargs.get("mongo_version")

        self._create_mongodb_monitor(db, **kwargs)

        db.save()
        return db

    def _delete_mongodb_monitor(self, db):
        raise NotImplementedError

    def delete_mongodb_monitor(self, identifier):
        db = MongoDbMonitor.objects(
            identifier=identifier,
            monitor_provider=self.provider,
            monitor_environment=self.environment
        ).get()
        self._delete_mongodb_monitor(db)
        db.delete()

    def get_mongodb_monitor(self, identifier_or_name):
        try:
            return MongoDbMonitor.objects(
                identifier=identifier_or_name,
                monitor_provider=self.provider,
                monitor_environment=self.environment
            ).get()
        except MongoDbMonitor.DoesNotExist:
            return None
