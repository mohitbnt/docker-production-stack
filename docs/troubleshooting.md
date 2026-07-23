# Troubleshooting

## Overview

This document lists common issues that may occur during local development or deployment, along with their likely causes and recommended resolutions.

---

## Common Issues

| Issue                            | Possible Cause                           | Resolution                                                                                           |
| -------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Containers fail to start         | Invalid or missing environment variables | Verify all required `.env` files are present and correctly configured.                               |
| Backend reports unhealthy        | PostgreSQL or Redis unavailable          | Confirm both services are running and reachable from the backend container.                          |
| Frontend cannot reach the API    | Nginx or backend configuration issue     | Verify the backend service is healthy and the Nginx configuration is correct.                        |
| Database connection failed       | Incorrect database configuration         | Check PostgreSQL credentials, hostname and Docker network connectivity.                              |
| Docker image build failed        | Dependency or Dockerfile issue           | Review the build logs and verify required files exist.                                               |
| Trivy scan failed                | Image unavailable or configuration issue | Ensure the Docker image was built successfully before scanning.                                      |
| GitHub Actions deployment failed | Workflow or AWS configuration issue      | Review the workflow logs and verify repository secrets and variables.                                |
| AWS SSM command failed           | EC2 instance unavailable or IAM issue    | Verify the instance is online, managed by Systems Manager, and associated with the correct IAM role. |
| Grafana dashboards are empty     | Prometheus target unavailable            | Confirm Prometheus is running and all configured targets are in an **UP** state.                     |
| Prometheus target DOWN           | Exporter unavailable                     | Verify the corresponding exporter container is running and reachable.                                |

---

## Useful Commands

View running containers:

```bash
docker compose -f compose/docker-compose.yaml ps
```

View container logs:

```bash
docker compose -f compose/docker-compose.yaml logs
```

Restart the application stack:

```bash
docker compose -f compose/docker-compose.yaml up -d
```

Check Docker networks:

```bash
docker network ls
```

Check Docker volumes:

```bash
docker volume ls
```

---

## Additional Resources

* [Architecture](architecture.md)
* [Deployment Guide](deployment.md)
* [CI/CD Pipeline](cicd.md)
* [Monitoring](monitoring.md)
* [Security](security.md)
