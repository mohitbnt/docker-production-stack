# Security

## Overview

Security is integrated into both the application architecture and the deployment pipeline. The project follows common DevOps security practices by using automated image scanning, secure AWS authentication, and environment-based configuration.

---

## Security Features

| Feature                       | Description                                                      |
| ----------------------------- | ---------------------------------------------------------------- |
| Trivy                         | Scans Docker images for known vulnerabilities                    |
| GitHub OIDC                   | Provides short-lived AWS credentials without storing access keys |
| AWS Systems Manager           | Enables deployments without SSH access                           |
| Environment Files             | Keeps configuration separate from application code               |
| Private Service Communication | Backend services communicate over an isolated Docker network     |

---

## Container Image Scanning

The CI/CD pipeline scans both backend and frontend Docker images using **Trivy** before deployment.

The scan:

* Detects known vulnerabilities
* Generates SARIF reports
* Uploads results to GitHub Security
* Provides visibility into image security before deployment

---

## AWS Authentication

GitHub Actions authenticates to AWS using **OpenID Connect (OIDC)**.

Benefits include:

* No long-lived AWS access keys
* Temporary credentials for each workflow run
* IAM role-based access control
* Improved security over static credentials

---

## Secure Deployment

Application deployment is performed using **AWS Systems Manager (SSM)**.

This approach provides:

* No SSH access required
* Centralized command execution
* Secure remote deployments
* Simplified operational management

---

## Current Security Practices

* Automated vulnerability scanning
* Secure AWS authentication
* Environment-specific configuration
* Private Docker networking
* Automated deployments through GitHub Actions

---

## Future Enhancements

Possible improvements include:

* Docker image signing
* Docker Secrets or AWS Secrets Manager
* Image vulnerability policy enforcement
* Container runtime security
* Dependency scanning

---

## Related Documentation

* [Architecture](architecture.md)
* [Deployment Guide](deployment.md)
* [CI/CD Pipeline](cicd.md)
* [Monitoring](monitoring.md)
* [Troubleshooting](troubleshooting.md)
