import logging
import json
from bson import json_util
from peewee import (
        MySQLDatabase, Model, DateTimeField, CharField,
        PrimaryKeyField, IntegerField, ForeignKeyField,
        fn
    )
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


db = MySQLDatabase(None)

class BaseModel(Model):

    class Meta:
        database = db

    @property
    def to_json(self):
        return json.dumps(self.__data__, default=json_util.default)

class DbmonitorCloud(BaseModel):
    nome = CharField()

    class Meta:
        table_name = 'dbmonitor_cloud'


class DbmonitorOrganizacao(BaseModel):
    nome = CharField(null=True)

    class Meta:
        table_name = 'dbmonitor_organizacao'


class DbmonitorServico(BaseModel):
    ambiente = CharField()
    ativo = IntegerField()
    descricao = CharField()
    url = CharField(null=True)

    class Meta:
        table_name = 'dbmonitor_servico'

class DbmonitorServidor(BaseModel):
    cloud = ForeignKeyField(
        column_name='cloud_id', field='id', model=DbmonitorCloud, null=True)
    dns = CharField()
    ip = CharField()
    memoria_mb = IntegerField(null=True)
    nome = CharField()
    organizacao = ForeignKeyField(
        column_name='organizacao_id',
        field='id',
        model=DbmonitorOrganizacao,
        null=True)
    quantidade_cpu = IntegerField(null=True)
    senha = CharField(null=True)
    tipo = CharField()
    tipo_so = CharField()
    usuario = CharField(null=True)

    class Meta:
        table_name = 'dbmonitor_servidor'

class DbmonitorServicoServidores(BaseModel):
    servico = ForeignKeyField(
        column_name='servico_id', field='id', model=DbmonitorServico)
    servidor = ForeignKeyField(
        column_name='servidor_id', field='id', model=DbmonitorServidor)

    class Meta:
        table_name = 'dbmonitor_servico_servidores'
        indexes = (
            (('servico', 'servidor'), True),
        )


class DbmonitorHandleModels(object):
    def __init__(self, database_endpoint):
        db = MySQLDatabase(**database_endpoint)
        DbmonitorCloud.bind(database=db)
        DbmonitorOrganizacao.bind(database=db)
        DbmonitorServidor.bind(database=db)

    def get_or_create_cloud(self, name):
        name = name.lower()
        cloud = DbmonitorCloud.get_or_none(
            fn.LOWER(DbmonitorCloud.nome) == name
        )
        if not cloud:
            msg = "Cloud not found: {}. It will be registered.".format(
                name)
            logging.info(msg)
            cloud = DbmonitorCloud.create(nome = name)
        return cloud.id

    def get_or_create_organization(self, name):
        name = name.lower()
        org = DbmonitorOrganizacao.get_or_none(
            fn.LOWER(DbmonitorOrganizacao.nome) == name
        )
        if not org:
            msg = "Organization not found: {}. It will be registered.".format(
                name)
            logging.info(msg)
            org = DbmonitorOrganizacao.create(nome = name)
        return org.id

    def create_host(self, credential, **kwargs):
        dns = kwargs.get("dns", None)
        ip = kwargs.get("ip", None)
        name = kwargs.get("name", None)
        machine_type = kwargs.get("machine_type", None)
        so_name = kwargs.get("so_name", None)
        cpu = kwargs.get("cpu", None)
        memory_mb = kwargs.get("memory_mb", None)
        organization_name = kwargs.get("organization_name", None)
        cloud_name = kwargs.get("cloud_name", None)
        service_name = kwargs.get("service_name", None)

        if not organization_name:
            organization_name = credential.default_organization_name

        if not cloud_name:
            cloud_name = credential.default_cloud_name

        if not machine_type:
            machine_type = credential.default_machine_type

        org_id = self.get_or_create_organization(organization_name)
        cloud_id  = self.get_or_create_cloud(cloud_name)

        machine_type = slugify(machine_type)
        if machine_type not in TIPO_MAQUINA.keys():
            msg = "machine_type must be in this list: {}".format(
                TIPO_MAQUINA_LIST)
            raise Exception(msg)
        machine_type_id = TIPO_MAQUINA[machine_type]

        service_id = self.get_service(service_name).id

        server = DbmonitorServidor(
            dns=dns,
            ip=ip,
            nome=name,
            tipo = machine_type_id,
            tipo_so = so_name,
            quantidade_cpu=cpu,
            memoria_mb=memory_mb,
            organizacao_id=org_id,
            cloud_id=cloud_id
        )
        server.save()

        servico_servidor = DbmonitorServicoServidores(
            servico = service_id,
            servidor = server.id
        )
        servico_servidor.save()

        return server.id

    def get_host(self, host_name):
        try:
            host = DbmonitorServidor.select(
                DbmonitorServidor.id, DbmonitorServidor.nome).where(
                DbmonitorServidor.nome == host_name).get()
        except DbmonitorServidor.DoesNotExist:
            raise Exception("Host {} does not exist".format(host_name))
        return host

    def delete_host(self, host_name):
        host = self.get_host(host_name)

        DbmonitorServicoServidores.delete().where(
            DbmonitorServicoServidores.servidor == host.id).execute()

        rows = DbmonitorServidor.delete().where(
            DbmonitorServidor.nome == host_name).execute()

    def get_service(self, service_name):
        try:
            service = DbmonitorServico.select(
                DbmonitorServico.id, DbmonitorServico.descricao).where(
                DbmonitorServico.descricao == service_name).get()
        except DbmonitorServico.DoesNotExist:
            raise Exception("Service {} does not exist".format(host_name))
        return service

    def create_service(self, credential, **kwargs):
        name = kwargs.get("name", None)
        url = kwargs.get("url", None)
        environment = kwargs.get("environment", None)

        if not environment:
            environment = credential.default_environment

        environment = slugify(environment)
        if environment not in TIPO_AMBIENTE.keys():
            msg = "Environment must be in this list: {}".format(
                TIPO_AMBIENTE_LIST)
            raise Exception(msg)
        environment_id = TIPO_AMBIENTE[environment]

        service = DbmonitorServico(
            descricao=name,
            url=url,
            ambiente=environment_id,
            ativo=True
        )
        service.save()
        return service.id

    def delete_service(self, service_id):
        rows = DbmonitorServico.delete().where(
            DbmonitorServico.id == service_id).execute()
        if rows == 0:
            raise Exception("Service id {} not found".format(service_id))
