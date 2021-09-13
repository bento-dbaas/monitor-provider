import logging
from pyzabbix import ZabbixAPI
from monitor_provider.credentials.zabbix import (
        CredentialZabbix, CredentialAddZabbix
    )
from monitor_provider.providers.base import ProviderBase
from monitor_provider.settings import LOGGING_LEVEL


logging.basicConfig(
    level=LOGGING_LEVEL,
    format='%(asctime)s %(filename)s(%(lineno)d) %(levelname)s: %(message)s')


class ProviderZabbix(ProviderBase):

    def __init__(self, environment):
        self._zapi = None
        super(ProviderZabbix, self).__init__(environment)

    @classmethod
    def get_provider(cls):
        return 'zabbix'

    def build_credential(self):
        return CredentialZabbix(self.provider, self.environment)

    def get_credential_add(self):
        return CredentialAddZabbix

    @property
    def zapi(self):
        if not self._zapi:
            self._zapi = ZabbixAPI(self.credential.endpoint)
            self._zapi.login(self.credential.user, self.credential.password)
        return self._zapi

    def _create_host_monitor(self, host, **kwargs):
        host.identifier = host.host_name
        host.environment = self.credential.default_environment
        host.locality = self.credential.default_locality
        host.hostgroups = self.credential.default_hostgroups
        host.alarm = self.credential.alarm
        data = {
            'host': host.host_name,
            'ip': host.ip,
            'environment': host.environment,
            'locality': host.locality,
            'hostgroups': host.hostgroups,
            'alarm': host.alarm
        }

        self.zapi.globo.createLinuxMonitors(**data)

    def _delete_host_monitor(self, host):
        data = {'host': host.identifier}
        self.zapi.globo.deleteMonitors(**data)

    def _create_web_monitor(self, web, **kwargs):

        mandatory_fields = ['host_name', 'url', 'required_string']
        self.check_mandatory_fields(mandatory_fields, **kwargs)

        web.environment = self.credential.default_environment
        web.locality = self.credential.default_locality
        web.hostgroups = self.credential.default_hostgroups
        web.alarm = self.credential.alarm
        web.url = kwargs.get("url", None)
        web.required_string = kwargs.get("required_string", None)

        web.host = web.url.replace('http://', 'web_')
        web.identifier = web.host.replace(':', '_').replace('/', '_')

        data = {
            'environment': web.environment,
            'locality': web.locality,
            'hostgroups': web.hostgroups,
            'alarm': web.alarm,
            'url': web.url,
            'required_string': web.required_string
        }

        self.zapi.globo.createWebMonitors(**data)

    def _delete_web_monitor(self, web):
        data = {'host': web.host}
        self.zapi.globo.deleteMonitors(**data)

    def _delete_tcp_monitor(self, tcp):
        data = {'host': tcp.identifier}
        self.zapi.globo.deleteMonitors(**data)

    def _create_tcp_monitor(self, tcp, **kwargs):
        if not tcp.environment:
            tcp.environment = self.credential.default_environment

        if not tcp.locality:
            tcp.locality = self.credential.default_locality

        if not tcp.hostgroups:
            tcp.hostgroups = self.credential.default_hostgroups

        if not tcp.alarm:
            tcp.alarm = self.credential.alarm

        tcp.identifier = "tcp_{}-{}".format(tcp.host, tcp.port)

        data = {
            'environment': tcp.environment,
            'locality': tcp.locality,
            'hostgroups': tcp.hostgroups,
            'host': tcp.host,
            'port': tcp.port,
            'alarm': tcp.alarm
        }

        opt = ('doc', 'notes', 'notification_email', 'notification_slack', 'zbx_proxy')
        for option in opt:
            if kwargs.get(option, None) is None:
                continue
            data[option] = kwargs.get(option)

        self.zapi.globo.createTCPMonitors(**data)

    def _delete_mysql_monitor(self, db):
        data = {'host': db.identifier}
        self.zapi.globo.deleteMonitors(**data)

    def _create_mysql_monitor(self, db, **kwargs):
        db.identifier = db.host

        if not db.environment:
            db.environment = self.credential.default_environment

        if not db.locality:
            db.locality = self.credential.default_locality

        if not db.hostgroups:
            db.hostgroups = self.credential.default_hostgroups

        if not db.alarm:
            db.alarm = self.credential.alarm

        data = {
            'environment': db.environment,
            'locality': db.locality,
            'hostgroups': db.hostgroups,
            'alarm': db.alarm,
            'host': db.host,
            'port': db.port,
            'user': db.user,
            'version': db.version,
            'password': kwargs.get('password'),
        }

        opt = (
            'clone', 'healthcheck', 'healthcheck_monitor', 'ssl_expire',
            'notification_email', 'notification_slack', 'slave_running',
            'notification_telegram', 'seconds_behind_master', 'ssl_support'
        )
        for option in opt:
            if kwargs.get(option, None) is None:
                continue
            data[option] = kwargs.get(option)

        self.zapi.globo.createMySQLMonitors(**data)
