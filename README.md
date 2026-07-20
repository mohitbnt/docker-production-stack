# OpsPortal

![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![React](https://img.shields.io/badge/React-Vite-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Project Overview

**OpsPortal** is a production-style IT Asset Management web application that has been fully containerized using Docker.

The primary objective of this repository is to demonstrate real-world DevOps practices rather than application development. The project showcases containerization, networking, persistent storage, service orchestration, automated database initialization, health checks, and production-ready Docker image creation.

This repository is intended as a portfolio project for demonstrating Docker and DevOps skills.

---

# Features

* Multi-stage Docker builds
* Production-ready Flask backend
* React + Vite frontend
* Nginx reverse proxy
* PostgreSQL database
* Redis cache
* Docker Compose orchestration
* Custom Docker bridge networks
* Persistent Docker volumes
* Health checks for all services
* Automatic database initialization
* Automatic application seeding
* Non-root application container
* OCI image metadata
* Environment-based configuration
* CI/CD-ready repository structure

---

# Technology Stack

| Layer             | Technology     |
| ----------------- | -------------- |
| Frontend          | React + Vite   |
| Backend           | Python Flask   |
| WSGI              | Gunicorn       |
| Reverse Proxy     | Nginx          |
| Database          | PostgreSQL 16  |
| Cache             | Redis 7        |
| Container Runtime | Docker Engine  |
| Orchestration     | Docker Compose |
| Operating System  | Ubuntu Server  |
| Package Manager   | npm / pip      |

---

# Architecture

```text
                        Internet
                            │
                            ▼
                   +-----------------+
                   |      Nginx      |
                   |  React Frontend |
                   +-----------------+
                            │
                            ▼
                  +-------------------+
                  | Flask API Backend |
                  |     Gunicorn      |
                  +-------------------+
                     │            │
                     ▼            ▼
             +-------------+   +---------+
             | PostgreSQL  |   |  Redis  |
             +-------------+   +---------+
```

---

# Docker Architecture

The application consists of four containers:

| Container    | Purpose                              |
| ------------ | ------------------------------------ |
| frontend-app | React application served by Nginx    |
| backend-app  | Flask REST API running with Gunicorn |
| postgres     | Primary relational database          |
| redis        | In-memory cache                      |

Each container has its own health check and participates in service dependency management.

---

# Networking

Two custom bridge networks are used.

```text
frontend-net
    │
    ├── frontend-app
    │
backend-net
    ├── frontend-app
    ├── backend-app
    ├── postgres
    └── redis
```

This isolates database services from direct external access while allowing communication between application components.

---

# Persistent Storage

Docker volumes are used to preserve data across container recreation.

| Volume        | Purpose           |
| ------------- | ----------------- |
| postgres-data | PostgreSQL data   |
| redis-data    | Redis persistence |

---

# Automatic Initialization

The application performs automatic initialization during deployment.

## PostgreSQL

Database schema and seed SQL files are executed automatically through:

```text
/docker-entrypoint-initdb.d/
```

## Backend

When the backend container starts it:

1. Waits for PostgreSQL
2. Verifies database connectivity
3. Seeds the application data (idempotent)
4. Creates the administrator account if it does not already exist
5. Starts Gunicorn

No manual database setup is required.

---

# Repository Structure

```text
opsportal/
│
├── backend/
├── frontend/
├── compose/
├── nginx/
├── redis/
├── backup/
├── docs/
├── scripts/
│
├── README.md
├── LICENSE
├── CHANGELOG.md
├── VERSION
├── .gitignore
└── .dockerignore
```

---

# Getting Started

## Prerequisites

* Docker Engine
* Docker Compose

Verify installation:

```bash
docker --version
docker compose version
```

---

# Clone Repository

```bash
git clone https://github.com/<your-github-username>/OpsPortal.git

cd OpsPortal
```

---

# Configure Environment

Copy the example environment files.

```bash
cp compose/.env.example compose/.env

cp compose/backend.env.example compose/backend.env

cp compose/frontend.env.example compose/frontend.env

cp compose/postgres.env.example compose/postgres.env
```

Update values as required.

---

# Build Images

```bash
cd compose

docker compose build
```

---

# Deploy

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
```

---

# Access Application

Open your browser:

```text
http://localhost
```

or

```text
http://<server-ip>
```

---

# Default Administrator

Configured through:

```text
compose/backend.env
```

Example:

```text
Email:
admin@opsportal.local

Password:
Admin@12345
```

The administrator account is automatically created during backend startup if it does not already exist.

---

# Health Checks

All services expose Docker health checks.

* PostgreSQL
* Redis
* Backend API
* Frontend (Nginx)

View status:

```bash
docker compose ps
```

---

# Screenshots

Login Page

```
docs/screenshots/login_page.png
```

Dashboard

```
docs/screenshots/dashboard.png
```

Running Containers

```
docs/screenshots/containers-compose.png
```

---

# Security Considerations

Current implementation includes:

* Non-root backend container
* Environment-based configuration
* Service isolation through Docker networks
* Persistent volumes
* Health monitoring
* OCI image metadata

Future enhancements:

* Docker Secrets
* TLS
* Trivy image scanning
* Image signing
* Rootless Docker
* Read-only containers
* Kubernetes Secrets

---

# Future Roadmap

## Completed

* Docker Compose
* Multi-stage frontend build
* Production backend image
* PostgreSQL
* Redis
* Nginx reverse proxy
* Health checks
* Automatic database initialization
* Automatic application seeding
* Persistent storage
* Custom Docker networks

## Planned

* GitHub Actions CI
* Docker Hub image publishing
* Amazon ECR image publishing
* Automated image versioning
* Trivy security scanning
* Terraform deployment
* AWS infrastructure
* Amazon ECS deployment
* Prometheus monitoring
* Grafana dashboards
* Kubernetes deployment

---

# Documentation

Additional documentation is available under:

```text
docs/
```

Including:

* Architecture
* Deployment
* Troubleshooting
* Screenshots

---

# License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

# Author

**Mohit Kumar**

Linux Administrator → DevOps Engineer

This repository is part of my DevOps learning journey, focusing on production-oriented Docker, infrastructure automation, CI/CD, Kubernetes, Terraform, and AWS.