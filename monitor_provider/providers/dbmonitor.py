from monitor_provider.credentials.dbmonitor import (
        CredentialDBMonitor, CredentialAddDBMonitor
    )
from monitor_provider.providers.base import ProviderBase
from monitor_provider.models.dbmonitor_models import (
    DbmonitorServico,
    DbmonitorCloud,
    DbmonitorServicoServidores,
    DbmonitorOrganizacao,
    DbmonitorServidor)
from peewee import MySQLDatabase, fn

from slugify import slugify

AMBIENTE_PRODUCAO = 'P'
AMBIENTE_DEV = 'D'
AMBIENTE_PRODUCAO_DESC = 'Produção'
AMBIENTE_DEV_DESC = 'DEV'
TIPO_AMBIENTE = {
    slugify(AMBIENTE_PRODUCAO_DESC): AMBIENTE_PRODUCAO,
    slugify(AMBIENTE_DEV_DESC): AMBIENTE_DEV
}
TIPO_AMBIENTE_LIST = (AMBIENTE_PRODUCAO_DESC, AMBIENTE_DEV_DESC)

MAQUINA_FISICA = '1'
MAQUINA_VIRTUAL = '2'
MAQUINA_FISICA_DESC = "Máquina Física"
MAQUINA_VIRTUAL_DESC = 'Máquina Virtual'
TIPO_MAQUINA = {
    slugify(MAQUINA_FISICA_DESC): MAQUINA_FISICA,
    slugify(MAQUINA_VIRTUAL_DESC): MAQUINA_VIRTUAL
}
TIPO_MAQUINA_LIST = (MAQUINA_FISICA_DESC, MAQUINA_VIRTUAL_DESC)



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

    @property
    def credential(self):
        if not self._credential:
            self._credential = self.build_credential()
        return self._credential

    def _create_service_monitor(self, service, **kwargs):
        service.url = kwargs.get("url", None)
        service.dbmonitor_environment = kwargs.get("environment", None)
        if not service.dbmonitor_environment:
            service.dbmonitor_environment = self.credential.default_environment

        dbmonitor_environment = slugify(service.dbmonitor_environment)
        if dbmonitor_environment not in TIPO_AMBIENTE.keys():
            msg = "Environment must be in this list: {}".format(
                TIPO_AMBIENTE_LIST)
            raise Exception(msg)
        service.dbmonitor_environment_id = TIPO_AMBIENTE[dbmonitor_environment]

        DbmonitorServico.bind(self.dbmonitor_database)
        dbmonitor_service = DbmonitorServico(
            descricao=service.name,
            url=service.url,
            ambiente=service.dbmonitor_environment_id,
            ativo=True
        )
        dbmonitor_service.save()
        service.identifier = str(dbmonitor_service.id)

    def _delete_service_monitor(self, service):
        DbmonitorServico.bind(self.dbmonitor_database)
        DbmonitorServico.delete().where(
            DbmonitorServico.id == service.identifier).execute()

    def _create_host_monitor(self, host, **kwargs):
        mandatory_fields = ['dns', 'ip', 'name', 'so_name', 'service_name']
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
            nome=host.name,
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

