# monitor-provider
Tsuru app to register Zabbix and DBMonitor Monitors
- Prod: `tsuru app-info -a monitor-provider`
- Dev: `tsuru app-info -a monitor-provider-dev`

## Concepts
1. Provider: name of the monitor service: zabbix or dbmonitor
2. Credential: credential to access the monitor service (endpoint, user, password, default parameters, etc)
2. Environment: credentials are related by environment

## Credentials

###### ADD

1. DBMonitor

```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/credential/new' -H 'Content-Type: application/json' -d '{{ "user": "database user", "password": "database passwoed", "host": "database endpoint", "port": database_port, "database": "database name", "default_cloud_name": "default cloud name", "default_organization_name": "default organization name", "default_machine_type": "machine type description", "default_environment": "default environment" }}
```

2. Zabbix

```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/credential/new' -H 'Content-Type: application/json' -d '{{"user": "api user", "password": "api password", "endpoint": "api endpoint", "default_environment": "default environment", "default_locality", "default locality", "default_hostgroups": "default hostgroup", "alarm": "alarm flag }}
```

###### GET

1. All provider credentials

```
curl -X GET '<monitor-provider_endpoint>/<provider_name>/credentials'
```

2. Environment provider credential

```
curl -X GET '<monitor-provider_endpoint>/<provider_name>/env/credential'
```

## Monitors

### Service Monitor (available only on DBMonitor)

###### ADD
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/service/new' -H 'Content-Type: application/json' -d '{"service_name": "service name",  "url": "url"}
```
Mandatory fields | Optional fields
------------ | -------------
service_name | url


###### GET
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/service/identifier_or_name'
```

###### DELETE
```
curl -X DELETE '<monitor-provider_endpoint>/<provider_name>/<env>/service/identifier'
```

### Host Monitor (available on both: DBMonitor and Zabbix)
###### ADD

```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/host/new' -H 'Content-Type: application/json' -d '{ "dns": "DNS", "ip": "IP Address", "host_name": "Host name", "so_name": "SO Name", "cpu": "number of CPUs", "memory_mb": "memory size in MB", "organization_name": "organization name", "cloud_name": "cloud name", "machine_type": "Machine type description", "service_name": "Service name"}'
```
Provider | Mandatory fields | Optional fields
------------ | -------------
DBMonitor | host_name, ip, dns, so_name, service_name | cpu, memory_mb, machine_type, organization_name, cloud_name
Zabbix | host_name, ip | dns, so_name, service_name | cpu, memory_mb, machine_type, organization_name, cloud_name,

###### GET
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/host/identifier_or_name'
```

###### DELETE
```
curl -X DELETE '<monitor-provider_endpoint>/<provider_name>/<env>/host/identifier'
```

### Web Monitor (available only on Zabbix)
###### ADD
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/web/new' -H 'Content-Type: application/json' -d '{"host_name": "host_name", "required_string": "WORKING", "url": "url"}'
```

Mandatory fields | Optional fields
------------ | -------------
host_name, url, required_string |


###### GET
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/web/identifier_or_name'
```

###### DELETE
```
curl -X DELETE '<monitor-provider_endpoint>/<provider_name>/<env>/web/identifier'
```
