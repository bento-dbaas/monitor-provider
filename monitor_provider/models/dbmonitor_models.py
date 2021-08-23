import logging
import json
from bson import json_util
from peewee import (
    MySQLDatabase, Model, DateTimeField, CharField,
    PrimaryKeyField, IntegerField, ForeignKeyField,
    fn, BooleanField
)
from slugify import slugify


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

class DbmonitorDatabase(BaseModel):
    nome = CharField()
    maquina = CharField()
    host_zabbix = CharField()
    sgbd = CharField()
    topologia = IntegerField()
    tipo = CharField()
    dns = CharField()
    host_db_zabbix = CharField()
    porta = CharField()
    versao = CharField()
    usuario = CharField()
    senha = CharField()
    ident_backup = CharField()
    ativo = BooleanField(default=True)
    flag_cluster = BooleanField(default=False)
    coleta_info_sessoes = BooleanField(default=False)
    coleta_info_tablespaces = BooleanField(default=False)
    coleta_info_segmentos = BooleanField(default=False)
    coleta_info_backup = BooleanField(default=False)
    coleta_info_key_buffer = BooleanField(default=False)
    testa_conexao = BooleanField(default=False)
    coleta_tamanho_database = BooleanField(default=False)
    flag_autenticacao = BooleanField(default=False)
    database_pai = ForeignKeyField(
        column_name='database_id',
        field='id',
        model='self',
        null=True)
    replicaset = CharField()
    testa_replicacao = BooleanField(default=False)
    testa_lock = BooleanField(default=False)
    disk_path = CharField()
    tipo_maquina = CharField()
    dbaas = BooleanField(default=True)
    organizacao = ForeignKeyField(
        column_name='organizacao_id',
        field='id',
        model=DbmonitorOrganizacao,
        null=True)
    cloud = ForeignKeyField(
        column_name='cloud_id',
        field='id',
        model=DbmonitorCloud,
        null=True)
    # agente = ForeignKey()
    testa_query_lenta = BooleanField(default=False)
    status_database = CharField()
    last_alive_status = DateTimeField()
    last_dead_status = DateTimeField()
    last_error = CharField()
    ssl_habilitado = BooleanField(default=False)
    ssl_obrigatorio = BooleanField(default=False)

    class Meta:
        table_name = 'dbmonitor_database'


class DbmonitorInstancia(BaseModel):
    database_id = ForeignKeyField(
        column_name='database_id',
        field='id',
        model=DbmonitorDatabase,
        null=True
    )
    nome = CharField()
    maquina = CharField()
    dns = CharField()
    porta = CharField()
    ativo = BooleanField(default=True)
    tipo_mongodb = CharField()
    disk_path = CharField()
    tipo_maquina = CharField()
    tipo_instancia = IntegerField()

    class Meta:
        table_name = 'dbmonitor_instancia'


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
