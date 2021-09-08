CASSANDRA = 'CASSANDRA'
POSTGRESQL = 'POSTGRESQL'

MANDATORY_FIELDS = {
    CASSANDRA: ['database_name', 'port', 'version', 'username', 'password'],
    POSTGRESQL: ['database_name', 'port', 'version', 'username', 'password', 'dns', 'topology']
}

SGBD_CASSANDRA = 'C'
SGBD_POSTGRESQL = 'P'
SGBD_CHOICES = {
    SGBD_CASSANDRA: "Cassandra",
    SGBD_POSTGRESQL: "PostgreSQL"
}

SGBD = {
    CASSANDRA: SGBD_CASSANDRA,
    POSTGRESQL: SGBD_POSTGRESQL
}

CASSANDRA_CLUSTER = 18
POSTGRESQL_SINGLE = 19
POSTGRESQL_STAND_BY = 20

TOPOLOGY = {
    'SINGLE': POSTGRESQL_SINGLE,
    'STANDBY': POSTGRESQL_STAND_BY
}

TOPOLOGIA_CHOICES = {
    CASSANDRA_CLUSTER: "Cassandra Cluster",
    POSTGRESQL_SINGLE: "PostgreSQL Single Instance",
    POSTGRESQL_STAND_BY: "PostgreSQL com Stand By Database"
}

INSTANCIA_POSTGRESQL = 16
INSTANCIA_POSTGRESQL_STAND_BY = 17
INSTANCIA_CASSANDRA = 18

INSTANCIA = {
    CASSANDRA_CLUSTER: INSTANCIA_CASSANDRA,
    POSTGRESQL_SINGLE: INSTANCIA_POSTGRESQL,
    POSTGRESQL_STAND_BY: INSTANCIA_POSTGRESQL_STAND_BY
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
