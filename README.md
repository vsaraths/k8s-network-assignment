
# Kubernetes Networking Troubleshooting Lab

A hands-on Kubernetes networking project that demonstrates how to deploy a multi-component application, validate communication between services, introduce networking failures, troubleshoot them, and verify recovery.

## Project Overview

The application consists of three components:

- **Client:** Sends HTTP requests to the frontend.
- **Frontend:** Exposes an `/orders` endpoint and calls the backend.
- **Backend:** Provides the `/orders` and `/health` endpoints.

The application runs on a Kubernetes cluster created with Kind. Docker is used to build the application images, and Kubernetes Deployments and ClusterIP Services manage the workloads and internal communication.

## Architecture

```text
Client
  |
  v
Frontend Service :8081
  |
  v
Frontend Pod
  |
  v
Backend Service :8080
  |
  v
Backend Pod
```

## Technologies Used

- Ubuntu on AWS EC2
- Docker
- Kubernetes
- Kind
- kubectl
- Python and Flask
- Kubernetes Deployments and Services
- NetworkPolicy

## Project Structure

| Directory/File | Purpose |
|---|---|
| `backend/` | Backend application and Docker configuration |
| `frontend/` | Frontend application and Docker configuration |
| `client/` | Client request application and Docker configuration |
| `k8s/` | Kubernetes Deployment and Service manifests |
| `docs/networking-issues.md` | Detailed networking troubleshooting report |

## Application Workflow

1. The client sends an HTTP request to the frontend Service.
2. Kubernetes routes the request to the frontend Pod.
3. The frontend calls the backend using `backend-service:8080`.
4. The backend returns an orders response.
5. The frontend returns the combined response to the client.

## Setup and Deployment

The project uses Docker images loaded into a Kind cluster. Kubernetes manifests in `k8s/` define the application Deployments and Services.

Typical workflow:

1. Build the client, frontend, and backend images.
2. Create the Kind cluster.
3. Load the images into Kind.
4. Apply the Kubernetes manifests.
5. Verify the Pods and Services.
6. Test the application through the frontend Service.

See the Kubernetes manifests in `k8s/` for the deployment configuration.

## Validation

Test the frontend-to-backend flow from inside the cluster:

```bash
kubectl run network-test --rm -i --restart=Never \
  --image=curlimages/curl:latest -- \
  curl -sS http://frontend-service:8081/orders
```

A successful request returns an orders response containing the frontend and backend service information.

## Networking Troubleshooting

The lab explores these networking failure scenarios:

1. Incorrect Service selector
2. Incorrect Service `targetPort`
3. Application listening on the wrong port
4. Service without endpoints
5. Incorrect DNS or Service name
6. NetworkPolicy blocking communication
7. Pod reachable directly but not through the Kubernetes Service

Each issue is introduced intentionally, investigated, resolved, and tested for recovery.

**Detailed findings:** [`docs/networking-issues.md`](docs/networking-issues.md)

## Learning Outcomes

- Understand Kubernetes Service discovery and DNS.
- Diagnose selector mismatches and missing endpoints.
- Troubleshoot application and Service port mismatches.
- Understand NetworkPolicy-based traffic restrictions.
- Compare direct Pod connectivity with Service connectivity.
- Validate recovery using `kubectl`, application logs, and HTTP requests.
