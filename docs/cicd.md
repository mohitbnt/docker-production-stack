# CI/CD Pipeline

## Overview

This project uses GitHub Actions to automate the build, security scanning, publishing, and deployment of the application. The pipeline eliminates manual deployment steps and provides a repeatable deployment process.

Production deployments use GitHub OIDC for authentication and AWS Systems Manager (SSM) for remote execution, removing the need for long-lived AWS credentials or SSH access.

---

## Pipeline Workflow

```text
Code Push
    │
    ▼
GitHub Actions
    │
    ├── Build Docker Images
    │
    ├── Trivy Security Scan
    │
    ├── Push Images to Docker Hub
    │
    ├── Authenticate to AWS (OIDC)
    │
    ├── Execute Deployment via AWS SSM
    │
    ▼
EC2 Instance
    │
    ├── Pull Latest Images
    ├── Restart Docker Compose Stack
    └── Remove Unused Images
```

---

## Pipeline Stages

| Stage          | Description                                                 |
| -------------- | ----------------------------------------------------------- |
| Checkout       | Retrieves the latest source code                            |
| Build          | Builds backend and frontend Docker images                   |
| Security Scan  | Scans images using Trivy for vulnerabilities                |
| Publish        | Pushes images to Docker Hub                                 |
| Authentication | Uses GitHub OIDC to assume an AWS IAM role                  |
| Deployment     | Deploys the updated application through AWS Systems Manager |

---

## Security

The deployment pipeline follows AWS security best practices:

* GitHub OIDC for short-lived AWS credentials
* No long-lived AWS access keys
* No SSH access required
* Automated container vulnerability scanning using Trivy
* Deployment executed through AWS Systems Manager

---

## Deployment Process

When changes are pushed to the configured branch, GitHub Actions automatically:

1. Builds updated container images.
2. Performs vulnerability scanning.
3. Pushes images to Docker Hub.
4. Connects securely to AWS using OIDC.
5. Executes deployment commands on the EC2 instance using SSM.
6. Pulls the latest images and recreates the required containers.

This process ensures consistent and repeatable deployments with minimal manual intervention.

---

## Related Documentation

* [Architecture](architecture.md)
* [Deployment Guide](deployment.md)
* [Monitoring](monitoring.md)
* [Security](security.md)
* [Troubleshooting](troubleshooting.md)
