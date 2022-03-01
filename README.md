# DemoApps

## 1. Description

This project holds test applications for practicing with:

- Kubernetes resources.
- Kubernetes patterns.
- Observability and monitorization.
- Industry standard applications.
- Etc.

I created a `docker-compose.yml` to make sure all the applications works correctly in a Kubernetes environment.

## 2. Applications

All the applications runs an HTTP web server with Python and Flask, and all of them have a Dockerfile. Each one has one functionality intended to test different characteristics in a Kuberbetes environment.

### 2.1. Random

With `GET /number` you'll get a random number between `1` and `1000`. This is the simplest application of all, with it you can test basic Kubernetes resources like Pods, Services, Deployments, ReplicaSets...

You can add to the REST call the query parameter `delay`, i.e. `GET /number?delay=10`. With that you specify the delay in seconds for the response. Useful to simulate process time.

### 2.2. EnvInspector

The endpoint `GET /envvars` will return a JSON with all environment variables that are visible by the application, useful to test ConfigMaps y Secrets.

### 2.3. Visits

With a call to `GET /count` a counter will be incremented and returned in the response body. This counter is stored in disk at `/tmp/visits.txt`, so this application could be used to test PersistentVolumes y los PersistentVolumeClaims.

### 2.4. Telemetry

This application has the following endpoints:

- `PUT /devices/{id}/temperature`: Requires the header `Content-Type: application/json` and a body like `{"temperature": 25.6}`. The specified temperature will be stored in Redis with the key corresponding to the device ID in the path. If that device ID don't exists, it will be created.
- `GET /devices/{id}/temperature`: The temperature for that device ID will be returned, obteined from Redis.
- `GET /devices`: Lists all the device IDs stored in Redis.

This is an application intended to communicate to other services, Redis in this case (which you can configure as you please, with or without persistence). This is a simple case but very similar to the way an application interacts with an RDBMS for example.

## 3. Other things you can test

- Jobs and CronJobs: These Kubernetes resources can use Bash commands with a base image in their definition. A simple `echo` command could be enough to test them, you don't need any other application.
- Industry standard applications:
  - A Docker registry like Harbor.
  - Infrastructure: Prometheus, Grafana, ArgoCD, ElasticSearch, Kibana, Logstash...
  - Data: Redis, PostgreSQL, MongoDB, InfluxDB...
  - Messaging: Mosquitto (MQTT), RabbitMQ...
  - Load balancers and web servers: HAProxy, Nginx, Apache...
- Serverless engines like Kubeless.
- Helm.
- Etc.

## 4. To-do applications

- An application that consumes large amounts of RAM, or large amounts CPU or crashes, everything through REST calls. It takes some time to start and must be compatible with readiness and liveness probes.
- An application that generates a lot of metrics to be ingested by other applications.
- An application to call external APIs to test Kubernetes patterns, VPNs, etc.
