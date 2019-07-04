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

### Service Monitor (available only DBMonitor)

###### ADD
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/service/new' -H 'Content-Type: application/json' -d '{"service_name": "service name",  "url": "url"}
```
Mandatory fields | Optional fields
------------ | -------------
service_name | service_name


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
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/host/new' -H 'Content-Type: application/json' -d '{"ip": "ip", "host_name": "host_name"}'
```
Mandatory fields on DBMonitor provider:

Optional fields on DBMonitor provider:

Mandatory fields on Zabbix provider:

Optional fields on Zabbix provider:


###### GET
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/host/identifier_or_name'
```

###### DELETE
```
curl -X DELETE '<monitor-provider_endpoint>/<provider_name>/<env>/host/identifier'
```

### Web Monitor (available only Zabbix)
###### ADD
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/web/new' -H 'Content-Type: application/json' -d '{"ip": "ip", "host_name": "host_name"}'
```

###### GET
```
curl -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/web/identifier_or_name'
```

###### DELETE
```
curl -X DELETE '<monitor-provider_endpoint>/<provider_name>/<env>/web/identifier'
```
