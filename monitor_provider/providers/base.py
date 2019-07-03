from monitor_provider.models.models import ServiceMonitor, HostMonitor


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
        mandatory_fields = ['name']
        self.check_mandatory_fields(mandatory_fields, **kwargs)
        name = kwargs.get("name")

        service = ServiceMonitor()
        service.provider = self.provider
        service.name = name
        self._create_service_monitor(service, **kwargs)

        service.save()
        return service

    def get_service_monitor(self, identifie_or_name):
        try:
            return ServiceMonitor.objects(
                identifier=identifie_or_name).get()
        except ServiceMonitor.DoesNotExist:
            pass
        try:
            return ServiceMonitor.objects(
                name=identifie_or_name).get()
        except ServiceMonitor.DoesNotExist:
            return None

    def _delete_service_monitor(self, service):
        raise NotImplementedError

    def delete_service_monitor(self, identifier):
        service = ServiceMonitor.objects(identifier=identifier).get()
        self._delete_service_monitor(service)
        service.delete()

    def _create_host_monitor(self, host, **kwargs):
        raise NotImplementedError

    def create_host_monitor(self, **kwargs):
        mandatory_fields = ['name', 'ip']
        self.check_mandatory_fields(mandatory_fields, **kwargs)
        name = kwargs.get("name")
        ip = kwargs.get("ip")

        host = HostMonitor()
        host.provider = self.provider
        host.name = name
        host.ip = ip

        self._create_host_monitor(host, **kwargs)

        host.save()
        return host

    def get_host_monitor(self, identifie_or_name):
        try:
            return HostMonitor.objects(
                identifier=identifie_or_name).get()
        except HostMonitor.DoesNotExist:
            pass
        try:
            return HostMonitor.objects(
                name=identifie_or_name).get()
        except ServiceMonitor.DoesNotExist:
            return None

    def _delete_host_monitor(self, host):
        raise NotImplementedError

    def delete_host_monitor(self, identifier):
        host = HostMonitor.objects(identifier=identifier).get()
        self._delete_host_monitor(host)
        host.delete()

    def create_web_monitor(self, ):
        pass

    def get_web_monitor(self, ):
        pass

    def delete_web_monitor(self, ):
        pass
