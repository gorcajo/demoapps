# DemoApps

## 1. Description

This project holds test applications for practicing with:

- Kubernetes resources.
- Kubernetes patterns.
- Observability and monitorization.
- Industry standard applications.
- Etc.

I created a `docker-compose.yml` to make sure all the applications works correctly in a containerized environment.

## 2. Applications

All the applications runs an HTTP web server with Python and Flask, and all of them have a Dockerfile. Each one has one functionality intended to test different characteristics in a Kuberbetes environment.

### 2.1. Random

With `GET /number` you'll get a random number between `1` and `1000`. This is the simplest application of all, with it you can test basic Kubernetes resources like Pods, Services, Deployments, ReplicaSets...

You can add to the REST call the query parameter `delay`, i.e. `GET /number?delay=10`. With that you specify the delay in seconds for the response. Useful to simulate process time.

### 2.2. EnvInspector

The endpoint `GET /envvars` will return a JSON with all environment variables that are visible by the application, useful to test ConfigMaps and Secrets.

### 2.3. Visits

With a call to `GET /count` a counter will be incremented and returned in the response body. This counter is stored in disk at `/tmp/visits.txt`, so this application could be used to test PersistentVolumes and PersistentVolumeClaims.

### 2.4. Telemetry

This application has the following endpoints:

- `PUT /devices/{id}/temperature`: Requires the header `Content-Type: application/json` and a body like `{"temperature": 25.6}`. The specified temperature will be stored in Redis with the key corresponding to the device ID in the path. If that device ID don't exists, it will be created.
- `GET /devices/{id}/temperature`: The temperature for that device ID will be returned, obteined from Redis.
- `GET /devices`: Lists all the device IDs stored in Redis.

This is an application intended to communicate to other services, Redis in this case (which you can configure as you please, with or without persistence). This is a simple case but very similar to the way an application interacts with an RDBMS for example.

## 3. To-Do

- An application that starts and ends, to test Jobs and CronJobs.
- An application that consumes large amounts of RAM, or large amounts CPU or crashes, everything through REST calls. It takes some time to start and must be compatible with readiness and liveness probes.
- An application that only reads a text file, to test Sidecar or InitContainer patterns.
- An application that generates metrics, to Prometheus to scrape them.
- An application to call external APIs (<https://wttr.in/:help>, <https://jsonplaceholder.typicode.com/>) to test NetworkPolicy and certain Kubernetes Patterns.
