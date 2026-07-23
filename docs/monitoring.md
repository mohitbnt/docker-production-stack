# Monitoring

## Overview

The project includes a built-in monitoring stack to provide visibility into both the Docker host and running containers. Metrics are collected by Prometheus and visualized through Grafana using automatically provisioned dashboards.

---

## Monitoring Stack

| Component     | Purpose                               |
| ------------- | ------------------------------------- |
| Prometheus    | Collects and stores metrics           |
| Grafana       | Visualizes metrics through dashboards |
| cAdvisor      | Provides container resource metrics   |
| Node Exporter | Provides host system metrics          |

---

## Monitoring Flow

```text
Docker Host ─┐
             ├──► Node Exporter ─┐
             │                   │
Containers ──┴──► cAdvisor ──────┤
                                 ▼
                           Prometheus
                                 │
                                 ▼
                             Grafana
```

---

## Available Dashboards

The following dashboards are automatically provisioned during deployment:

| Dashboard          | Description                                                           |
| ------------------ | --------------------------------------------------------------------- |
| Node Exporter Full | CPU, memory, disk, filesystem and network metrics for the Docker host |
| cAdvisor Full      | CPU, memory, filesystem and network usage for Docker containers       |

Dashboard provisioning is managed through the Grafana provisioning configuration included in this repository.

---

## Metrics Collected

Host Metrics:

* CPU utilization
* Memory usage
* Disk utilization
* Filesystem usage
* Network traffic

Container Metrics:

* CPU usage
* Memory consumption
* Network traffic
* Filesystem usage
* Running container status

---

## Access

Once the monitoring stack is running:

* **Grafana** – Dashboard visualization
* **Prometheus** – Metrics collection and querying

Refer to the `compose/docker-compose.yaml` file for the configured service ports.

---

## Related Documentation

* [Architecture](architecture.md)
* [Deployment Guide](deployment.md)
* [CI/CD Pipeline](cicd.md)
* [Security](security.md)
* [Troubleshooting](troubleshooting.md)
