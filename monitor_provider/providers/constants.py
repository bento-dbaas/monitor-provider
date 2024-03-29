CASSANDRA = 'cassandra'
POSTGRESQL = 'postgresql'
MYSQL = 'mysql'
MONGODB = 'mongodb'

VALID_DBMS = (CASSANDRA, POSTGRESQL, MYSQL, MONGODB)

MANDATORY_FIELDS = {
    CASSANDRA: ['database_name', 'port', 'version', 'username', 'password'],
    POSTGRESQL: ['database_name', 'port', 'version', 'username', 'password', 'dns', 'topology'],
    MYSQL: ['database_name', 'port', 'version', 'username', 'password', 'dns', 'topology'],
    MONGODB: ['database_name', 'port', 'version', 'username', 'password', 'dns', 'topology']
}

SGBD_CASSANDRA = 'C'
SGBD_MYSQL = 'M'
SGBD_POSTGRESQL = 'P'
SGBD_MONGODB = 'G'
SGBD_CHOICES = {
    SGBD_CASSANDRA: "Cassandra",
    SGBD_POSTGRESQL: "PostgreSQL",
    SGBD_MYSQL: 'MySQL',
    SGBD_MONGODB: 'MongoDB'
}

SGBD = {
    CASSANDRA: SGBD_CASSANDRA,
    MYSQL: SGBD_MYSQL,
    POSTGRESQL: SGBD_POSTGRESQL,
    MONGODB: SGBD_MONGODB
}

MYSQL_SINGLE = 1
MYSQL_FOXHA = 3
MONGODB_SINGLE = 9
MONGODB_REPLICA_SET = 10
CASSANDRA_CLUSTER = 18
POSTGRESQL_SINGLE = 19
POSTGRESQL_STAND_BY = 20

TOPOLOGY = {
    'POSTGRESQL_SINGLE': POSTGRESQL_SINGLE,
    'POSTGRESQL_STANDBY': POSTGRESQL_STAND_BY,
    'MYSQL_SINGLE': MYSQL_SINGLE,
    'MYSQL_FOXHA': MYSQL_FOXHA,
    'MONGODB_SINGLE': MONGODB_SINGLE,
    'MONGODB_REPLICA_SET': MONGODB_REPLICA_SET
}

TOPOLOGIA_CHOICES = {
    CASSANDRA_CLUSTER: "Cassandra Cluster",
    POSTGRESQL_SINGLE: "PostgreSQL Single Instance",
    POSTGRESQL_STAND_BY: "PostgreSQL com Stand By Database",
    MYSQL_SINGLE: "MySQL Single Instance",
    MYSQL_FOXHA: "MySQL FOXHA",
    MONGODB_SINGLE: "MongoDB Single Instance",
    MONGODB_REPLICA_SET: "MongoDB Replica Set"
}

INSTANCIA_MYSQL = 1
INSTANCIA_MONGODB = 4
INSTANCIA_MONGODB_ARBITER = 5
INSTANCIA_POSTGRESQL = 16
INSTANCIA_POSTGRESQL_STAND_BY = 17
INSTANCIA_CASSANDRA = 18

INSTANCIA = {
    CASSANDRA_CLUSTER: INSTANCIA_CASSANDRA,
    POSTGRESQL_SINGLE: INSTANCIA_POSTGRESQL,
    POSTGRESQL_STAND_BY: INSTANCIA_POSTGRESQL_STAND_BY,
    MYSQL_FOXHA: INSTANCIA_MYSQL
}

INSTANCIA_CHOICES = {
    'INSTANCIA_MONGODB': INSTANCIA_MONGODB,
    'INSTANCIA_MONGODB_ARBITER': INSTANCIA_MONGODB_ARBITER
}


class Constants:
    def __init__(self, dbms, **kwargs):
        self.dbms = dbms
        self.kwargs = kwargs
        self._set_db_constants()

    def _set_db_constants(self):
        if self.dbms == CASSANDRA:
            self._topology_id = CASSANDRA_CLUSTER
        else:
            try:
                topology_code = self.kwargs.get('topology')
                self._topology_id = TOPOLOGY[topology_code]
            except KeyError:
                raise Exception(
                    "Invalid topology choice. "
                    "Please choose one of the following: {}".format(
                        list(TOPOLOGY.keys())
                    )
                )

        self._topology_name = TOPOLOGIA_CHOICES[self._topology_id]
        self._sgbd_id = SGBD[self.dbms]
        self._sgbd_name = SGBD_CHOICES[self._sgbd_id]

    @property
    def topology_id(self):
        return self._topology_id

    @property
    def topology_name(self):
        return self._topology_name

    @property
    def sgbd_id(self):
        return self._sgbd_id

    @property
    def sgbd_name(self):
        return self._sgbd_name
