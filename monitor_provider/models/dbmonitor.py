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
