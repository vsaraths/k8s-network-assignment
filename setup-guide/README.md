# Kubernetes Lab Setup Guide

## 1. Overview

This guide explains how to build and deploy the client, frontend, and backend applications on a fresh Ubuntu EC2 instance using Docker, Kind, and Kubernetes.

## 2. Architecture

- Client: Sends HTTP requests to the frontend.
- Frontend: Receives requests on port 8081 and calls the backend.
- Backend: Returns an orders response on port 8080.
- Kubernetes Services provide internal networking and DNS discovery.

Request flow:

`Client → frontend-service:8081 → Frontend Pod → backend-service:8080 → Backend Pod`

## 3. Prerequisites

- Ubuntu EC2 instance with internet access.
- SSH or EC2 Instance Connect access.
- GitHub repository access.
- Sufficient memory and disk space for Docker and Kind.

## 4. Install Required Tools

### Update Ubuntu and install utilities

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg git
```

### Install Docker Engine

```bash
sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verify Docker:

```bash
sudo docker run hello-world
```

Configure Docker permissions:

```bash
sudo usermod -aG docker "$USER"
newgrp docker
docker run hello-world
```

### Install kubectl

```bash
sudo snap install kubectl --classic
kubectl version --client
```

### Install Kind

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64

chmod +x ./kind

sudo mv ./kind /usr/local/bin/kind

kind version
```

## 5. Clone the Project

```bash
git clone https://github.com/vsaraths/k8s-network-assignment.git

cd k8s-network-assignment
```

Verify the project files:

```bash
ls
ls backend frontend client
```

## 6. Build Docker Images

Build each application image from the repository root:

```bash
docker build -t imesh-backend:1.0 ./backend

docker build -t imesh-frontend:1.0 ./frontend

docker build -t imesh-client:1.0 ./client
```

Verify:

```bash
docker images | grep imesh
```

Expected images:

- `imesh-backend:1.0`
- `imesh-frontend:1.0`
- `imesh-client:1.0`

Ensure the frontend reads the `BACKEND_URL` environment variable using `os.getenv()`.

## 7. Create the Kind Cluster

```bash
kind create cluster --name imesh-lab
```

Verify the node:

```bash
kubectl get nodes
```

Wait until the node status is `Ready`.

## 8. Load Docker Images into Kind

```bash
kind load docker-image imesh-backend:1.0 --name imesh-lab

kind load docker-image imesh-frontend:1.0 --name imesh-lab

kind load docker-image imesh-client:1.0 --name imesh-lab
```

This makes the locally built images available to Kubernetes without pushing them to a container registry.

## 9. Deploy Kubernetes Resources

Apply the manifests:

```bash
kubectl apply -f k8s/backend.yaml

kubectl apply -f k8s/frontend.yaml

kubectl apply -f k8s/client.yaml
```

Check Pods and Services:

```bash
kubectl get pods -o wide
kubectl get services
kubectl get endpointslices
```

Wait until the application Pods are ready.

## 10. Verify Application Connectivity

Test the frontend and backend through the frontend Service:

```bash
kubectl run network-test --rm -i --restart=Never \
  --image=curlimages/curl:latest -- \
  curl -sS http://frontend-service:8081/orders
```

Expected response includes:

- `service: frontend`
- `service: backend`
- `Orders retrieved successfully`

Check the client:

```bash
kubectl logs deployment/client --tail=20
```

Successful requests should display `Request successful!`.

## 11. Troubleshooting a Service Selector Mismatch

### Introduce the issue

Change the backend Service selector to an incorrect label:

```bash
kubectl patch service backend-service \
  -p '{"spec":{"selector":{"app":"wrong-backend"}}}'
```

### Investigate

```bash
kubectl get pods --show-labels

kubectl get services

kubectl get endpointslices \
  -l kubernetes.io/service-name=backend-service

kubectl logs deployment/client --since=2m
```

The backend Service has no matching endpoints, and frontend requests return HTTP 500.

### Root cause

The Service selector `app: wrong-backend` does not match the backend Pod label `app: backend`.

### Restore the correct selector

```bash
kubectl patch service backend-service \
  -p '{"spec":{"selector":{"app":"backend"}}}'
```

### Verify recovery

```bash
kubectl get endpointslices \
  -l kubernetes.io/service-name=backend-service
```

The EndpointSlice should show the backend Pod IP and port 8080.

Repeat the connectivity test from Section 10. Confirm that the orders response succeeds.

## 12. Cleanup

Delete the lab cluster when finished:

```bash
kind delete cluster --name imesh-lab
```

Stop or terminate the EC2 instance when it is no longer needed to avoid unnecessary cloud charges.

## 13. Key Learning Outcomes

- Building container images using Docker.
- Running Kubernetes locally on EC2 with Kind.
- Deployments, Pods, Services, and Kubernetes DNS.
- Troubleshooting Service selectors and EndpointSlices.
- Using application logs and repeatable tests to verify recovery.
