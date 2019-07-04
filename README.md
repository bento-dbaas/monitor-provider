# monitor-provider
Tsuru app to register Zabbix and DBMonitor Monitors
- Prod: `tsuru app-info -a monitor-provider`
- Dev: `tsuru app-info -a monitor-provider-dev`

## Concepts
1. Provider: name of the monitor service: zabbix or dbmonitor
2. Credential: credential to access the monitor service (endpoint, user, password, default parameters, etc)
2. Environment: credentials are related by environment

## Credentials

## Monitors

### Service Monitor (available only DBMonitor)
###### ADD
```
curl -u 'username:password' -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/service/new' -H 'Content-Type: application/json' -d '{"**service_name**": "service name",  "url": "url"}
```
###### GET
###### DELETE

### Host Monitor (available both DBMonitor and Zabbix)
###### ADD

```
curl -u 'username:password' -X POST '<monitor-provider_endpoint>/<provider_name>/<env>/service/new' -H 'Content-Type: application/json' -d '{"ip": "ip", "host_name": "host_name"}'
```
When the provider is DBMonitor, must include these fields:

  dns
  so_name
  cpu
  memory_mb
  service_name


###### GET
###### DELETE

### Web Monitor (available only Zabbix)
###### ADD
###### GET
###### DELETE
