# Deployment Guide

## Overview

This project can be deployed locally using Docker Compose or automatically to AWS through the included GitHub Actions pipeline.

The AWS infrastructure (EC2 instance, IAM roles, GitHub OIDC provider, and related resources) is provisioned separately using the companion Terraform repository.

**Related Repository:** `github-oidc-aws_platform_terraform`

---

## Prerequisites

Before deploying the project, ensure the following requirements are met:

* Docker Engine
* Docker Compose
* Git
* Docker Hub account
* GitHub repository with Actions enabled

For AWS deployment, provision the infrastructure using the Terraform repository before running the CI/CD pipeline.

---

## Local Deployment

Clone the repository and configure the required environment files.

```bash
cp compose/.env.example compose/.env
cp compose/backend.env.example compose/backend.env
cp compose/frontend.env.example compose/frontend.env
cp compose/postgres.env.example compose/postgres.env
```

Start the application:

```bash
docker compose -f compose/docker-compose.yaml up -d
```

Verify all containers are running:

```bash
docker compose -f compose/docker-compose.yaml ps
```

The application and monitoring services are now available on their configured ports.

---

## AWS Deployment

Production deployments are fully automated using GitHub Actions.

The workflow performs the following steps:

1. Build Docker images
2. Scan images with Trivy
3. Push images to Docker Hub
4. Authenticate to AWS using GitHub OIDC
5. Execute deployment commands on the EC2 instance through AWS Systems Manager (SSM)
6. Pull the latest images and restart the Docker Compose stack

No SSH access is required during deployment.

---

## GitHub Configuration

Configure the required repository secrets and variables before running the pipeline.

Examples include:

**Secrets**

* Docker Hub credentials
* AWS account information (if applicable)

**Variables**

* AWS Region
* EC2 Instance ID
* Docker image version
* Docker Hub username

Refer to the GitHub Actions workflow (`.github/workflows/ci-cd.yml`) for the complete list of required values.

---

## Updating the Application

To deploy a new version:

1. Commit and push changes to the repository.
2. GitHub Actions builds new container images.
3. Images are scanned and pushed to Docker Hub.
4. The EC2 instance automatically pulls the updated images.
5. Docker Compose recreates the affected containers with minimal manual intervention.

---

## Related Documentation

* [Architecture](architecture.md)
* [CI/CD Pipeline](cicd.md)
* [Monitoring](monitoring.md)
* [Security](security.md)
* [Troubleshooting](troubleshooting.md)
