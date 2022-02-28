# DemoApps

## 1. Descripción

Proyecto con aplicaciones de pruebas para practicar con:

- Recursos de Kubernetes.
- Patrones de Kubernetes.
- Balanecadores de carga o aplicaciones como HA Proxy o Nginx.
- Observabilidad y monitorización con Prometheus y Grafana o el stack ELK.
- Etc.

## 2. Aplicaciones

Todas las aplicaciones levantan un servidor HTTP con Python y Flask y disponen de su correspondiente `Dockerfile`. Cada una tiene una funcionalidad distinta, pensada para probar distintas características de un entorno con Kubernetes.

### 2.1. Random

Mediante un `GET /number` se obtiene un número aleatorio entre `1` y `1000`. Es la aplicación más sencilla de todas, pensada para probar los recusos básicos de Kubernetes como Pods, Services, Deployments, RecplicaSets...

### 2.2. EnvInspector

El endpoint `GET /envvars` devuelve un JSON con todas las variables de entorno visibles por la aplicación. La utilidad de esta aplicación puede ser probar los ConfigMaps y Secrets.

### 2.3. Visits

Realizando una llamada a `GET /count` se incrementa un contador de visitas y se devuelve por el body de la respuesta. El contador se almacena en disco, en la ruta `/tmp/visits.txt`, por lo que esta aplicación puede ser útil para probar los PersistentVolumes y los PersistentVolumeClaims.

### 2.4. Telemetry

Esta aplicación tiene tres endpoints:

- `PUT /devices/{id}/temperature`: Requiere la cabecera `Content-Type: application/json` y un body similar a `{"temperature": 25.6}`. De esta manera, se almacenará en Redis la temperatura indicada en el body en la clave correspondiente al `id` del dispositivo, en el path de la petición.
- `GET /devices/{id}/temperature`: Se obtiene la temperatura almacenada en Redis, con la clave indicada en la `id` del path de la petición.
- `GET /devices`: Lista todas las IDs de los dispositivos almacenados en Redis.

Es una aplicación pensada para levantar otros servicios y lograr comunicarlos entre sí. En este caso se requiere un Redis, el cual podría ser a su vez configurado para persistir los datos. Es un caso sencillo pero es muy similar a la forma de interactuar con un RDBMS.

## 3. Mejoras futuras

- Proceso batch, para probar los CronJobs.
- Aplicación cuyas peticiones tarden un tiempo no despreciable de proceso, para probar balanceadores de carga.
- Aplicación que genere muchas métricas para ser ingestadas por otras aplicaciones de infraestructura.
- Aplicación que llame a aplicaciones externas, para probar patrones de kubernetes, VPNs, o lo que sea.
- Compatibilidad de todas las aplicaciones con readiness y liveness probes.
- Traducir este readme al inglés...
