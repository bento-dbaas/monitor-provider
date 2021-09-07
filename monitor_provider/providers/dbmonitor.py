from monitor_provider.providers.constants import Constants

from monitor_provider.credentials.dbmonitor import (
        CredentialDBMonitor, CredentialAddDBMonitor
    )
from monitor_provider.providers.base import ProviderBase
from monitor_provider.models.dbmonitor_models import (
    DbmonitorServico,
    DbmonitorCloud,
    DbmonitorServicoServidores,
    DbmonitorOrganizacao,
    DbmonitorServidor,
    DbmonitorDatabase,
    DbmonitorInstancia)
from peewee import MySQLDatabase, fn
from slugify import slugify

AMBIENTE_PRODUCAO = 'P'
AMBIENTE_DEV = 'D'
AMBIENTE_PRODUCAO_DESC = 'PROD'
AMBIENTE_DEV_DESC = 'DEV'
TIPO_AMBIENTE = {
    slugify(AMBIENTE_PRODUCAO_DESC): AMBIENTE_PRODUCAO,
    slugify(AMBIENTE_DEV_DESC): AMBIENTE_DEV
}
TIPO_AMBIENTE_LIST = (AMBIENTE_PRODUCAO_DESC, AMBIENTE_DEV_DESC)

DATABASE_PRODUCAO = 'P'
DATABASE_DEV = 'Q'
DATABASE_PRODUCAO_DESC = 'PROD'
DATABASE_DEV_DESC = 'DEV'
AMBIENTE_DATABASE = {
    slugify(DATABASE_PRODUCAO_DESC): DATABASE_PRODUCAO,
    slugify(DATABASE_DEV_DESC): DATABASE_DEV
}
TIPO_AMBIENTE_DATABASE = (DATABASE_PRODUCAO_DESC, DATABASE_DEV_DESC)

MAQUINA_FISICA = '1'
MAQUINA_VIRTUAL = '2'
MAQUINA_FISICA_DESC = "Máquina Física"
MAQUINA_VIRTUAL_DESC = 'Máquina Virtual'
TIPO_MAQUINA = {
    slugify(MAQUINA_FISICA_DESC): MAQUINA_FISICA,
    slugify(MAQUINA_VIRTUAL_DESC): MAQUINA_VIRTUAL
}
TIPO_MAQUINA_LIST = (MAQUINA_FISICA_DESC, MAQUINA_VIRTUAL_DESC)

SGBD_CASSANDRA = 'C'
SGBD_CHOICES = {
    SGBD_CASSANDRA: "Cassandra",
}

CASSANDRA_CLUSTER = 18
TOPOLOGIA_CHOICES = {
    CASSANDRA_CLUSTER: "Cassandra Cluster",
}

INSTANCIA_CASSANDRA = 18


class ProviderDBMonitor(ProviderBase):

    def __init__(self, environment):
        super(ProviderDBMonitor, self).__init__(environment)
        self._dbmonitor_database = None

    @classmethod
    def get_provider(cls):
        return 'dbmonitor'

    def build_credential(self):
        return CredentialDBMonitor(self.provider, self.environment)

    def get_credential_add(self):
        return CredentialAddDBMonitor

    @property
    def dbmonitor_database(self):
        if not self._dbmonitor_database:
            self._dbmonitor_database = MySQLDatabase(
                **self.credential.database_endpoint)
        return self._dbmonitor_database

    def get_database_monitor_dns(self, database_id):
        DbmonitorDatabase.bind(self.dbmonitor_database)
        dns = DbmonitorDatabase.get_by_id(database_id).dns

        try:
            return dns.split(',')
        except AttributeError:
            return []

    def set_database_monitor_dns(self, database_id, dns):
        dns_str = ','.join(dns)
        DbmonitorDatabase.bind(self.dbmonitor_database)
        DbmonitorDatabase.update(
            {DbmonitorDatabase.dns: dns_str}
        ).where(
            DbmonitorDatabase.id == database_id
        ).execute()

    @property
    def credential(self):
        if not self._credential:
            self._credential = self.build_credential()
        return self._credential

    def _create_service_monitor(self, service, **kwargs):
        service.url = kwargs.get("url", None)
        service.environment = kwargs.get("environment", None)
        if not service.environment:
            service.environment = self.credential.default_environment

        environment = slugify(service.environment)
        if environment not in TIPO_AMBIENTE.keys():
            msg = "Environment must be in this list: {}".format(
                TIPO_AMBIENTE_LIST)
            raise Exception(msg)
        service.environment_id = TIPO_AMBIENTE[environment]

        DbmonitorServico.bind(self.dbmonitor_database)
        dbmonitor_service = DbmonitorServico(
            descricao=service.service_name,
            url=service.url,
            ambiente=service.environment_id,
            ativo=True
        )
        dbmonitor_service.save()
        service.identifier = str(dbmonitor_service.id)

    def _delete_service_monitor(self, service):
        DbmonitorServico.bind(self.dbmonitor_database)
        DbmonitorServico.delete().where(
            DbmonitorServico.id == service.identifier).execute()

    def _create_database_monitor(self, dbms, dbms_name, **kwargs):
        constants = Constants(dbms_name)
        dbms.topology_type_id = constants.topology_id
        dbms.topology_name = constants.topology_name
        dbms.sgbd_type_id = constants.sgbd_id
        dbms.sgbd = constants.sgbd_name

        if not dbms.environment:
            dbms.environment = self.credential.default_environment
        environment = slugify(dbms.environment)
        if environment not in AMBIENTE_DATABASE.keys():
            msg = "Environment must be in this list: {}".format(
                TIPO_AMBIENTE_DATABASE)
            raise Exception(msg)
        dbms.environment_id = AMBIENTE_DATABASE[environment]

        if not dbms.cloud_name:
            dbms.cloud_name = self.credential.default_cloud_name
        dbms.cloud_id  = self.get_cloud_by_name(dbms.cloud_name)

        if not dbms.machine_type:
            dbms.machine_type = self.credential.default_machine_type
        machine_type = slugify(dbms.machine_type)

        if machine_type not in TIPO_MAQUINA.keys():
            msg = "machine_type must be in this list: {}".format(
                TIPO_MAQUINA_LIST)
            raise Exception(msg)
        dbms.machine_type_id = TIPO_MAQUINA[machine_type]

        password = fn.ENCODE(
            kwargs.get('password'), self.credential.decode_key
        )

        DbmonitorDatabase.bind(self.dbmonitor_database)
        database = DbmonitorDatabase(
            ativo=dbms.active,
            nome=dbms.database_name,
            tipo=dbms.environment_id,
            tipo_maquina = dbms.machine_type_id,
            porta=dbms.port,
            versao=dbms.version,
            usuario=dbms.username,
            senha=password,
            cloud_id=dbms.cloud_id,
            sgbd=dbms.sgbd_type_id,
            topologia=dbms.topology_type_id
        )

        database.save()
        dbms.identifier = str(database.id)

    def _delete_database_monitor(self, sgbd):
        DbmonitorDatabase.bind(self.dbmonitor_database)
        DbmonitorDatabase.update({DbmonitorDatabase.ativo: False}).where(
            DbmonitorDatabase.id == int(sgbd.identifier)
        ).execute()

    def _create_instance_cassandra_monitor(self, instance, **kwargs):
        if not instance.machine_type:
            instance.machine_type = self.credential.default_machine_type
        machine_type = slugify(instance.machine_type)

        if machine_type not in TIPO_MAQUINA.keys():
            msg = "machine_type must be in this list: {}".format(
                TIPO_MAQUINA_LIST)
            raise Exception(msg)
        instance.machine_type_id = TIPO_MAQUINA[machine_type]

        DbmonitorInstancia.bind(self.dbmonitor_database)
        db_instance = DbmonitorInstancia(
            database_id=instance.database_id,
            dns=instance.dns,
            tipo_mongodb=None,
            disk_path=instance.disk_path,
            tipo_maquina=instance.machine_type_id,
            tipo_instancia=INSTANCIA_CASSANDRA,
            nome=instance.instance_name,
            maquina=instance.machine,
            porta=instance.port,
            ativo=instance.active,
        )

        db_instance.save()

        dns_list = self.get_database_monitor_dns(instance.database_id)
        dns_list.append(instance.dns)
        self.set_database_monitor_dns(instance.database_id, dns_list)

        instance.identifier = str(db_instance.id)

    def _delete_instance_monitor(self, instance):
        DbmonitorInstancia.bind(self.dbmonitor_database)
        DbmonitorInstancia.update({DbmonitorInstancia.ativo: False}).where(
            DbmonitorInstancia.id == int(instance.identifier)
        ).execute()

        dns_list = self.get_database_monitor_dns(instance.database_id)
        dns_list.remove(instance.dns)
        self.set_database_monitor_dns(instance.database_id, dns_list)

    def _create_host_monitor(self, host, **kwargs):
        mandatory_fields = ['dns', 'ip', 'host_name', 'so_name', 'service_name']
        self.check_mandatory_fields(mandatory_fields, **kwargs)
        host.dns = kwargs.get("dns", None)
        host.so_name = kwargs.get("so_name", None)
        host.cpu = kwargs.get("cpu", None)
        host.memory_mb = kwargs.get("memory_mb", None)
        host.machine_type = kwargs.get("machine_type", None)
        host.organization_name = kwargs.get("organization_name", None)
        host.cloud_name = kwargs.get("cloud_name", None)
        host.service_name = kwargs.get("service_name", None)


        if not host.organization_name:
            host.organization_name = self.credential.default_organization_name
        host.organization_id = self.get_organization_by_name(
            host.organization_name)

        if not host.cloud_name:
            host.cloud_name = self.credential.default_cloud_name
        host.cloud_id  = self.get_cloud_by_name(host.cloud_name)

        if not host.machine_type:
            host.machine_type = self.credential.default_machine_type

        machine_type = slugify(host.machine_type)
        if machine_type not in TIPO_MAQUINA.keys():
            msg = "machine_type must be in this list: {}".format(
                TIPO_MAQUINA_LIST)
            raise Exception(msg)
        host.machine_type_id = TIPO_MAQUINA[machine_type]

        service = self.get_service_monitor(host.service_name)
        if not service:
            msg = 'Service {} not found'.format(host.service_name)
            raise Exception(msg)
        host.service_id = int(service.identifier)

        DbmonitorServidor.bind(self.dbmonitor_database)
        dbmonitor_host = DbmonitorServidor(
            dns=host.dns,
            ip=host.ip,
            nome=host.host_name,
            tipo = host.machine_type_id,
            tipo_so = host.so_name,
            quantidade_cpu=host.cpu,
            memoria_mb=host.memory_mb,
            organizacao_id=host.organization_id,
            cloud_id=host.cloud_id
        )
        dbmonitor_host.save()
        host.identifier = str(dbmonitor_host.id)

        DbmonitorServicoServidores.bind(self.dbmonitor_database)
        dbmonitor_servico_servidor = DbmonitorServicoServidores(
            servico = host.service_id,
            servidor = dbmonitor_host.id
        )
        dbmonitor_servico_servidor.save()

    def _delete_host_monitor(self, host):

        DbmonitorServicoServidores.bind(self.dbmonitor_database)
        DbmonitorServicoServidores.delete().where(
            DbmonitorServicoServidores.servidor == int(host.identifier)
        ).execute()

        DbmonitorServidor.bind(self.dbmonitor_database)
        DbmonitorServidor.delete().where(
            DbmonitorServidor.id == int(host.identifier)
        ).execute()


    def get_cloud_by_name(self, name):
        DbmonitorCloud.bind(self.dbmonitor_database)
        name = name.lower()
        cloud = DbmonitorCloud.get_or_none(
            fn.LOWER(DbmonitorCloud.nome) == name
        )
        if not cloud:
            msg = "Cloud {} not found.".format(name)
            logging.error(msg)
            raise Exception(msg)
        return cloud.id

    def get_organization_by_name(self, name):
        DbmonitorOrganizacao.bind(self.dbmonitor_database)
        name = name.lower()
        org = DbmonitorOrganizacao.get_or_none(
            fn.LOWER(DbmonitorOrganizacao.nome) == name
        )
        if not org:
            msg = "Organization {} not found.".format(name)
            logging.error(msg)
            raise Exception(msg)
        return org.id

