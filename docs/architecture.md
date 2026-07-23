# Architecture

## Overview

This project demonstrates a production-oriented Docker deployment of a sample Flask and React application. The focus is on containerization, networking, reverse proxy configuration, monitoring, security scanning, and automated deployment rather than application development.

The application stack consists of a React frontend, Flask API backend, PostgreSQL database, Redis cache, and Nginx reverse proxy. Operational visibility is provided by Prometheus, Grafana, cAdvisor, and Node Exporter, while GitHub Actions automates image building, security scanning, publishing, and deployment to AWS.

---

## Architecture

```
                        Internet
                            │
                            ▼
                      Nginx Reverse Proxy
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
        React Frontend              Flask Backend
                                            │
                              ┌─────────────┴─────────────┐
                              ▼                           ▼
                         PostgreSQL                   Redis

────────────────────────────────────────────────────────────────

Node Exporter ─┐
cAdvisor ──────┼────► Prometheus ─────► Grafana
               │
Docker Host ───┘
```

---

## Project Components

| Component     | Purpose                                                        |
| ------------- | -------------------------------------------------------------- |
| Nginx         | Reverse proxy serving the frontend and forwarding API requests |
| Frontend      | React application providing the user interface                 |
| Backend       | Flask REST API handling business logic                         |
| PostgreSQL    | Persistent relational database                                 |
| Redis         | Caching and session storage                                    |
| Prometheus    | Metrics collection                                             |
| Grafana       | Metrics visualization                                          |
| cAdvisor      | Container metrics exporter                                     |
| Node Exporter | Host system metrics exporter                                   |

---

## Container Networking

The project uses dedicated Docker bridge networks to isolate application traffic.

| Network          | Connected Services                |
| ---------------- | --------------------------------- |
| Frontend Network | Nginx                             |
| Backend Network  | Backend, PostgreSQL, Redis, Nginx |

Only Nginx is exposed externally. Backend services communicate internally over the private backend network.

---

## Persistent Storage

Persistent Docker volumes are used to retain application data between container restarts.

* PostgreSQL database
* Grafana configuration and dashboards
* Prometheus time-series data

---

## Configuration

Application configuration is managed using environment files stored under the `compose/` directory.

Example files are included for all required services:

* `.env.example`
* `backend.env.example`
* `frontend.env.example`
* `postgres.env.example`

These files provide a template for creating environment-specific configurations without storing sensitive information in the repository.

---

## Deployment Overview

Deployment is fully automated through GitHub Actions.

Pipeline stages:

1. Build Docker images
2. Scan images with Trivy
3. Push images to Docker Hub
4. Authenticate to AWS using GitHub OIDC
5. Deploy to EC2 through AWS Systems Manager (SSM)
6. Update the running Docker Compose stack

AWS infrastructure required for deployment is provisioned separately using Terraform.

Related repository:

**github-oidc-aws_platform_terraform**

---

## Design Decisions

* Multi-stage Docker builds to reduce image size.
* Docker Compose for local and production orchestration.
* Nginx used as the single public entry point.
* Separate frontend and backend networks for service isolation.
* Environment-specific configuration using `.env` files.
* Infrastructure managed separately with Terraform.
* Automated deployments using GitHub Actions, AWS OIDC, and AWS Systems Manager.
* Monitoring and security integrated into the deployment pipeline.

---

## Related Documentation

* [Deployment Guide](deployment.md)
* [CI/CD Pipeline](cicd.md)
* [Monitoring](monitoring.md)
* [Security](security.md)
* [Troubleshooting](troubleshooting.md)
